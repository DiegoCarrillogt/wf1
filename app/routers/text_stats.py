from fastapi import APIRouter, HTTPException
from models.schemas import TextStatsRequest
from services import text_stats_service

router = APIRouter(
    prefix="/text-stats",
    tags=["text analysis"]
)

@router.post("/analyze")
async def analyze_text(request: TextStatsRequest):
    """
    Analyze text and return various statistics including:
    - Text length
    - Word count
    - Sentence count
    - Average word length
    - Readability score
    - Word frequency (optional)
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