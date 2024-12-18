from fastapi import APIRouter
from services import sentiment_service

router = APIRouter(
    prefix="/sentiment-analysis",
    tags=["sentiment"]
)

@router.get("/{text}")
def analyze_sentiment(text: str):
    """Analyze the sentiment of the provided text."""
    return sentiment_service.analyze_sentiment(text) 