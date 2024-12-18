from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from textblob import TextBlob
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import json

class SearchResult(BaseModel):
    position: int
    title: str
    link: str
    source: str
    domain: str
    displayed_link: str
    snippet: str
    snippet_highlighted_words: List[str]
    favicon: str

class KeyRemovalRequest(BaseModel):
    collection: List[List[Dict[str, Any]]]  # Array of arrays of dictionaries
    keysToRemove: List[str]

app = FastAPI(title="Sentiment Analysis API")

@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs", status_code=308)

@app.get("/sentiment-analysis/{text}")
def sentiment_analysis(text: str):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0:
        sentiment = "positive"
    elif polarity < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "text": text,
        "sentiment": sentiment,
        "polarity": polarity,
        "subjectivity": subjectivity
    }

@app.post("/removeKeys")
def remove_keys(request: KeyRemovalRequest):
    # Get the inner array (first element of the outer array)
    collection = request.collection[0] if request.collection else []
    keys_to_remove = request.keysToRemove
    
    # Remove specified keys from each item in the collection
    for item in collection:
        for key in keys_to_remove:
            if key in item:
                del item[key]
    
    # Return the modified collection wrapped in an array to maintain format
    return [collection]

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8001)
