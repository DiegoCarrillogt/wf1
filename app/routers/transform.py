from fastapi import APIRouter, HTTPException
from models.schemas import TransformationRequest
from services import transform_service

router = APIRouter(
    prefix="/transform",
    tags=["transform"]
)

@router.post("", summary="Transform Data", description="Transform JSON data based on a mapping configuration")
def transform_data(request: TransformationRequest):
    """
    Transform JSON data based on a mapping configuration.
    
    Example request:
    ```json
    {
        "data": {
            "user": {
                "personal": {
                    "firstName": "John",
                    "lastName": "Doe"
                },
                "contact": {
                    "email": "john@example.com"
                }
            }
        },
        "mapping": {
            "name": "user.personal.firstName",
            "email": "user.contact.email"
        }
    }
    ```
    
    You can also transform arrays using array_path:
    ```json
    {
        "data": {
            "users": [
                {"name": "John", "age": 30},
                {"name": "Jane", "age": 25}
            ]
        },
        "mapping": {
            "user_name": "name",
            "user_age": "age"
        },
        "array_path": "users"
    }
    ```
    """
    return transform_service.transform_data(
        request.data,
        request.mapping,
        request.array_path,
        request.preserve_null
    ) 