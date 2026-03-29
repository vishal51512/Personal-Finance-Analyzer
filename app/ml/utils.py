import joblib

# load full pipeline (vectorizer + model)
model = joblib.load("app/ml/model.pkl")


def predict_category(description, merchant=None):
    text = f"{merchant or ''} {description}"
    return model.predict([text])[0]