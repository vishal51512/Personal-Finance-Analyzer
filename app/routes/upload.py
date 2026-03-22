from fastapi import APIRouter, UploadFile, File
import pandas as pd

router = APIRouter()

@router.post("/upload-transactions")
async def upload_transactions(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    # convert to dict
    data = df.to_dict(orient="records")

    return {
        "message": "File uploaded successfully",
        "preview": data[:5]
    }