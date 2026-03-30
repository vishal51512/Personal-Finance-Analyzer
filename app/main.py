from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, analytics

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(analytics.router)

@app.get("/")
def home():
    return {"message": "Finance Analyzer Backend Running 🚀"}
