import pandas as pd

# global storage (temporary)
TRANSACTIONS = []


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


def process_file(file):
    global TRANSACTIONS

    df = pd.read_csv(file)
    df = clean_data(df)

    TRANSACTIONS = df  # store dataframe

    return df.to_dict(orient="records")

def get_analytics():
    global TRANSACTIONS

    if TRANSACTIONS is None or len(TRANSACTIONS) == 0:
        return {"message": "No data available"}

    df = TRANSACTIONS.copy()

    # only debit = spending
    spending = df[df['amount'] < 0]

    # total spending
    total_spent = abs(spending['amount'].sum())

    # category (simple keyword-based)
    def categorize(desc):
        desc = desc.lower()
        if "swiggy" in desc or "zomato" in desc:
            return "Food"
        elif "amazon" in desc or "flipkart" in desc:
            return "Shopping"
        elif "uber" in desc or "ola" in desc:
            return "Travel"
        else:
            return "Others"

    spending['category'] = spending['description'].apply(categorize)

    # category breakdown
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

    return {
        "total_spent": float(total_spent),
        "category_breakdown": category_data,
        "monthly_trend": monthly_data
    }