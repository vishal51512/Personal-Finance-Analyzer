import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


def predict_next_month(df):
    # only spending
    df = df[df['amount'] < 0].copy()

    if df.empty:
        return {"prediction": "No spending data"}

    # convert date
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])

    # monthly aggregation
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month')['amount'].sum().abs().reset_index()

    # sort (IMPORTANT)
    monthly = monthly.sort_values('month')

    if len(monthly) < 2:
        return {"prediction": "Not enough data"}

    # create index
    monthly['month_index'] = np.arange(len(monthly))

    X = monthly[['month_index']]
    y = monthly['amount']

    # train model
    model = LinearRegression()
    model.fit(X, y)

    # ✅ FIX: use DataFrame (no warning)
    next_index = pd.DataFrame({'month_index': [len(monthly)]})
    prediction = model.predict(next_index)[0]

    # 🔥 EXTRA: trend direction
    trend = "increasing" if model.coef_[0] > 0 else "decreasing"

    return {
        "predicted_spending_next_month": float(prediction),
        "trend": trend
    }