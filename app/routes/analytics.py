from fastapi import APIRouter
from app.services.transaction_service import get_analytics

router = APIRouter()

@router.get("/analytics")
def analytics():
    return get_analytics()