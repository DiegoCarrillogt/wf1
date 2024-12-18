from fastapi import APIRouter, HTTPException
from models.schemas import TextStatsRequest
from services import text_stats_service

router = APIRouter(
    prefix="/text-stats",
    tags=["text analysis"]
)

@router.post("/analyze", summary="Analyze Text Statistics", description="Analyze text and return various statistics")
async def analyze_text(request: TextStatsRequest):
    """
    Analyze text and return various statistics including:
    - Text length
    - Word count
    - Sentence count
    - Average word length
    - Readability score
    - Word frequency (optional)
    
    Example request:
    ```json
    {
        "text": "This is a sample text. It contains multiple sentences and some repeated words.",
        "include_word_freq": true
    }
    ```
    """
    try:
        return text_stats_service.analyze_text_stats(
            request.text,
            request.include_word_freq
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 