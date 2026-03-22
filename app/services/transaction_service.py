import pandas as pd
from app.db.supabase import supabase


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


# ✅ Save to Supabase
def save_to_supabase(df):
    data = df.to_dict(orient="records")

    # ensure JSON serializable
    for row in data:
        row['date'] = str(row['date'])
        row['amount'] = float(row['amount'])

    try:
        response = supabase.table("transactions").insert(data).execute()
        return response
    except Exception as e:
        raise Exception(f"Supabase insert failed: {str(e)}")


def process_file(file):
    df = pd.read_csv(file)
    df = clean_data(df)

    save_to_supabase(df)

    # return safe JSON
    data = df.to_dict(orient="records")

    for row in data:
        row['date'] = str(row['date'])

    return data


# ✅ Analytics
def get_analytics():
    try:
        response = supabase.table("transactions").select("*").execute()
        data = response.data
    except Exception as e:
        return {"error": str(e)}

    if not data:
        return {"message": "No data available"}

    df = pd.DataFrame(data)

    df['amount'] = df['amount'].astype(float)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    spending = df[df['amount'] < 0].copy()

    total_spent = abs(spending['amount'].sum())

    def categorize(desc):
        desc = str(desc).lower()
        if "swiggy" in desc or "zomato" in desc:
            return "Food"
        elif "amazon" in desc or "flipkart" in desc:
            return "Shopping"
        elif "uber" in desc or "ola" in desc:
            return "Travel"
        else:
            return "Others"

    spending['category'] = spending['description'].apply(categorize)

    category_data = (
        spending.groupby('category')['amount']
        .sum()
        .abs()
        .to_dict()
    )

    spending['month'] = spending['date'].dt.to_period('M').astype(str)

    monthly_data = (
        spending.groupby('month')['amount']
        .sum()
        .abs()
        .to_dict()
    )

    return {
        "total_spent": float(total_spent),
        "category_breakdown": category_data,
        "monthly_trend": monthly_data
    }