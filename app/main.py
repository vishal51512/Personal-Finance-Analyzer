from fastapi import FastAPI
from app.routes import upload
from app.routes import upload, analytics

app = FastAPI()

app.include_router(upload.router)
app.include_router(analytics.router)

@app.get("/")
def home():
    return {"message": "Finance Analyzer Backend Running 🚀"}