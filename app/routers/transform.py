from fastapi import APIRouter
from models.schemas import TransformationRequest
from services import transform_service

router = APIRouter(
    prefix="/transform",
    tags=["transform"]
)

@router.post("")
def transform_data(request: TransformationRequest):
    """Transform JSON data based on a mapping configuration."""
    return transform_service.transform_data(
        request.data,
        request.mapping,
        request.array_path,
        request.preserve_null
    ) 