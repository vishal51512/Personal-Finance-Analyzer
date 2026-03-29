import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier


# =========================
# 📊 Better Dataset
# =========================
data = {
    "description": [
        "Swiggy order", "Zomato food", "Uber ride", "Ola cab",
        "Amazon shopping", "Flipkart order", "Electricity bill",
        "Netflix subscription", "Salary credit",
        "Petrol pump", "Gas bill", "Movie ticket",
        "Train booking", "Flight ticket", "Restaurant dinner",
        "Grocery shopping", "Milk purchase"
    ],
    "category": [
        "Food", "Food", "Travel", "Travel",
        "Shopping", "Shopping", "Bills",
        "Bills", "Income",
        "Travel", "Bills", "Entertainment",
        "Travel", "Travel", "Food",
        "Food", "Food"
    ]
}

df = pd.DataFrame(data)


# =========================
# 🧠 PIPELINE (IMPORTANT)
# =========================
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(lowercase=True, stop_words="english")),
    ("model", RandomForestClassifier(n_estimators=100))
])

# train
pipeline.fit(df["description"], df["category"])


# =========================
# 💾 SAVE (single file)
# =========================
joblib.dump(pipeline, "app/ml/model.pkl")

print("✅ Model trained & saved 🚀")