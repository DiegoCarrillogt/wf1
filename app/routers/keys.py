from fastapi import APIRouter, HTTPException
from models.schemas import KeyRemovalRequest
from services import key_service

router = APIRouter(
    prefix="/keys",
    tags=["keys"]
)

@router.post("/remove", summary="Remove Keys", description="Remove specified keys from a collection of objects")
def remove_keys(request: KeyRemovalRequest):
    """
    Remove specified keys from each object in the collection.
    
    Example request:
    ```json
    {
        "collection": [[
            {"id": 1, "name": "John", "age": 30, "extra": "remove_me"},
            {"id": 2, "name": "Jane", "age": 25, "extra": "remove_me"}
        ]],
        "keysToRemove": ["extra", "age"]
    }
    ```
    """
    try:
        return key_service.remove_keys(request.collection, request.keysToRemove)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error removing keys: {str(e)}"
        ) 