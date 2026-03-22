import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


def predict_next_month(df):
    # only spending
    df = df[df['amount'] < 0].copy()

    # convert date
    df['date'] = pd.to_datetime(df['date'])

    # monthly aggregation
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby('month')['amount'].sum().abs().reset_index()

    if len(monthly) < 2:
        return {"prediction": "Not enough data"}

    # convert month to index
    monthly['month_index'] = np.arange(len(monthly))

    X = monthly[['month_index']]
    y = monthly['amount']

    # train model
    model = LinearRegression()
    model.fit(X, y)

    # predict next month
    next_index = [[len(monthly)]]
    prediction = model.predict(next_index)[0]

    return {
        "predicted_spending_next_month": float(prediction)
    }