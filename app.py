from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from textblob import TextBlob
from pydantic import BaseModel
from typing import List
import uvicorn
import json

class KeyRemovalRequest(BaseModel):
    collection: List[dict]
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
    collection = request.collection
    keys_to_remove = request.keysToRemove
    
    # Remove specified keys from each item in the collection
    for item in collection:
        for key in keys_to_remove:
            if key in item:
                del item[key]
    
    return collection

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8001)
