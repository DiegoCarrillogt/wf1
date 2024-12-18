from fastapi import APIRouter, HTTPException
from services import sentiment_service

router = APIRouter(
    prefix="/sentiment-analysis",
    tags=["sentiment"]
)

@router.get("/{text}", summary="Analyze Sentiment", description="Analyze the sentiment of the provided text")
def analyze_sentiment(text: str):
    """
    Analyze the sentiment of the provided text and return:
    - Sentiment (positive, negative, or neutral)
    - Polarity score (-1 to 1)
    - Subjectivity score (0 to 1)
    
    Example:
    ```
    GET /sentiment-analysis/This is a great day!
    ```
    
    Response:
    ```json
    {
        "text": "This is a great day!",
        "sentiment": "positive",
        "polarity": 0.8,
        "subjectivity": 0.75
    }
    ```
    """
    try:
        return sentiment_service.analyze_sentiment(text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing sentiment: {str(e)}"
        ) 