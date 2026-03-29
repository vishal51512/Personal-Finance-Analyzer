import pandas as pd
import tempfile
from app.db.supabase import supabase
from app.ml.utils import predict_category
from sklearn.ensemble import IsolationForest
from app.ml.predict import predict_next_month
from app.utils.parser import parse_file


# =========================
# 🧹 CLEAN DATA
# =========================
def clean_data(df):
    df.columns = df.columns.str.lower().str.strip()

    required_cols = ['date', 'description', 'amount']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    df['amount'] = (
        df['amount']
        .astype(str)
        .replace('[₹, ]', '', regex=True)
        .astype(float)
    )

    df['type'] = df['amount'].apply(lambda x: 'debit' if x < 0 else 'credit')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    df = df.dropna(subset=['date', 'amount'])

    return df


# =========================
# 🧠 MERCHANT CLEANING
# =========================
def clean_merchant(text):
    text = str(text).lower()

    if "zomato" in text:
        return "zomato"
    elif "swiggy" in text:
        return "swiggy"
    elif "amazon" in text:
        return "amazon"
    elif "uber" in text:
        return "uber"
    elif "flipkart" in text:
        return "flipkart"

    return text[:30]


# =========================
# 💾 SAVE TO SUPABASE
# =========================
def save_to_supabase(df):
    data = df.to_dict(orient="records")

    for row in data:
        row['date'] = str(row['date'])

    try:
        response = supabase.table("transactions").insert(data).execute()
        return response
    except Exception as e:
        print("❌ Supabase insert failed:", e)
        return None


# =========================
# 📤 PROCESS FILE
# =========================
def process_file(file, user_id=None):
    if user_id is None:
        user_id = "test_user"

    filename = file.filename

    # -------- CSV --------
    if filename.endswith(".csv"):
        df = pd.read_csv(file.file)
        df = clean_data(df)

    # -------- OTHER FILES --------
    else:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.file.read())
            temp_path = tmp.name

        df = parse_file(temp_path)
        df = clean_data(df)

    # -------- FEATURES --------
    df['merchant'] = df['description'].apply(clean_merchant)
    df['user_id'] = user_id

    # 🔥 ML CATEGORY (FAST)
    texts = (df['merchant'].fillna('') + " " + df['description']).tolist()
    df['category'] = [predict_category(text) for text in texts]

    # balance tracking
    df = df.sort_values("date")
    df['balance'] = df['amount'].cumsum()

    # save to DB
    save_to_supabase(df)

    # return JSON safe
    data = df.to_dict(orient="records")
    for row in data:
        row['date'] = str(row['date'])

    return data


# =========================
# 📊 ANALYTICS + ML
# =========================
def get_analytics(user_id):
    try:
        response = supabase.table("transactions") \
            .select("*") \
            .eq("user_id", user_id) \
            .execute()

        data = response.data

    except Exception as e:
        return {"error": str(e)}

    if not data:
        return {"message": "No data available"}

    df = pd.DataFrame(data)

    df['amount'] = df['amount'].astype(float)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # =========================
    # 📈 PREDICTION
    # =========================
    prediction_result = predict_next_month(df)

    # only spending
    spending = df[df['amount'] < 0].copy()

    total_spent = abs(spending['amount'].sum())

    # =========================
    # 🤖 CATEGORY (FAST)
    # =========================
    texts = (spending['merchant'].fillna('') + " " + spending['description']).tolist()
    spending['category'] = [predict_category(text) for text in texts]

    category_data = (
        spending.groupby('category')['amount']
        .sum()
        .abs()
        .to_dict()
    )

    # =========================
    # 🏆 TOP CATEGORIES
    # =========================
    top_categories = (
        spending.groupby('category')['amount']
        .sum()
        .abs()
        .sort_values(ascending=False)
        .head(3)
        .to_dict()
    )

    # =========================
    # 📅 MONTHLY TREND
    # =========================
    spending['month'] = spending['date'].dt.to_period('M').astype(str)

    monthly_data = (
        spending.groupby('month')['amount']
        .sum()
        .abs()
        .to_dict()
    )

    # =========================
    # 🚨 ANOMALY DETECTION
    # =========================
    spending['day'] = spending['date'].dt.day
    spending['weekday'] = spending['date'].dt.weekday
    spending['month_num'] = spending['date'].dt.month

    features = spending[['amount', 'day', 'weekday', 'month_num']]

    model = IsolationForest(contamination=0.05)
    spending['anomaly'] = model.fit_predict(features)

    anomalies = spending[spending['anomaly'] == -1]

    anomaly_data = anomalies[['description', 'amount']].to_dict(orient="records")

    return {
        "total_spent": float(total_spent),
        "category_breakdown": category_data,
        "top_categories": top_categories,
        "monthly_trend": monthly_data,
        "prediction": prediction_result,
        "anomalies": anomaly_data
    }