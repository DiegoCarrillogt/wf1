from fastapi import APIRouter, HTTPException
from models.schemas import KeyRemovalRequest
from services import key_service

router = APIRouter(
    prefix="/keys",
    tags=["keys"]
)

@router.post("/remove")
def remove_keys(request: KeyRemovalRequest):
    """Remove specified keys from a collection."""
    try:
        return key_service.remove_keys(request.collection, request.keysToRemove)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error removing keys: {str(e)}"
        ) 