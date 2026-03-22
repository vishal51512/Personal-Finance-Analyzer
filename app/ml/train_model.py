import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

# sample training data
data = {
    "description": [
        "Swiggy order", "Zomato food", "Uber ride", "Ola cab",
        "Amazon shopping", "Flipkart order", "Electricity bill",
        "Netflix subscription", "Salary credit"
    ],
    "category": [
        "Food", "Food", "Travel", "Travel",
        "Shopping", "Shopping", "Bills",
        "Bills", "Income"
    ]
}

df = pd.DataFrame(data)

# text → features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["description"])

# model
model = RandomForestClassifier()
model.fit(X, df["category"])

# save model
joblib.dump(model, "app/ml/model.pkl")
joblib.dump(vectorizer, "app/ml/vectorizer.pkl")

print("Model trained and saved 🚀")