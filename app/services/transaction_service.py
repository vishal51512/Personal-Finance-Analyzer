import pandas as pd
from app.db.supabase import supabase
from app.ml.utils import predict_category
from sklearn.ensemble import IsolationForest
from app.ml.predict import predict_next_month


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
        .replace('[₹,]', '', regex=True)
        .astype(float)
    )

    df['type'] = df['amount'].apply(lambda x: 'debit' if x < 0 else 'credit')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    df = df.dropna(subset=['date', 'amount'])

    return df


# =========================
# 💾 SAVE TO SUPABASE
# =========================
def save_to_supabase(df):
    data = df.to_dict(orient="records")

    for row in data:
        row['date'] = str(row['date'])
        row['amount'] = float(row['amount'])

    try:
        return supabase.table("transactions").insert(data).execute()
    except Exception as e:
        raise Exception(f"Supabase insert failed: {str(e)}")


# =========================
# 📤 PROCESS FILE (NO user_id)
# =========================
def process_file(file):
    df = pd.read_csv(file)
    df = clean_data(df)

    save_to_supabase(df)

    data = df.to_dict(orient="records")

    for row in data:
        row['date'] = str(row['date'])

    return data


# =========================
# 📊 ANALYTICS + ML (NO user_id)
# =========================
def get_analytics():
    try:
        response = supabase.table("transactions") \
            .select("*") \
            .execute()

        data = response.data

    except Exception as e:
        return {"error": str(e)}

    if not data:
        return {"message": "No data available"}

    df = pd.DataFrame(data)

    # safe conversion
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
    # 🤖 ML CATEGORY
    # =========================
    spending['category'] = spending['description'].apply(predict_category)

    category_data = (
        spending.groupby('category')['amount']
        .sum()
        .abs()
        .to_dict()
    )

    # monthly trend
    spending['month'] = spending['date'].dt.to_period('M').astype(str)

    monthly_data = (
        spending.groupby('month')['amount']
        .sum()
        .abs()
        .to_dict()
    )

    # =========================
    # 🚨 ANOMALY DETECTION (SAFE)
    # =========================
    if len(spending) > 1:
        anomaly_model = IsolationForest(contamination=0.1)
        spending['anomaly'] = anomaly_model.fit_predict(spending[['amount']])
        anomalies = spending[spending['anomaly'] == -1]
    else:
        anomalies = pd.DataFrame()

    anomaly_data = anomalies[['description', 'amount']].to_dict(orient="records")

    return {
        "total_spent": float(total_spent),
        "category_breakdown": category_data,
        "monthly_trend": monthly_data,
        "prediction": prediction_result,
        "anomalies": anomaly_data
    }