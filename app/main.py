from fastapi import FastAPI
from app.routes import upload

app = FastAPI()

app.include_router(upload.router)

@app.get("/")
def home():
    return {"message": "Finance Analyzer Backend Running 🚀"}