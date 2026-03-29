from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.transaction_service import process_file
from app.utils.auth import verify_token

router = APIRouter()

@router.post("/upload-transactions")
async def upload_transactions(
    file: UploadFile = File(...),
):
    try:
        data = process_file(file)  # ✅ pass user_id

        return {
            "message": "File uploaded successfully",
            "preview": data[:5],
            "total_records": len(data)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))