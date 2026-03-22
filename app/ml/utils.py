import joblib

import joblib

model = joblib.load("app/ml/model.pkl")
vectorizer = joblib.load("app/ml/vectorizer.pkl")


def predict_category(description):
    X = vectorizer.transform([description])
    return model.predict(X)[0]