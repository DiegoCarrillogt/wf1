from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from textblob import TextBlob
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
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
    collection: List[List[Dict[str, Any]]]
    keysToRemove: List[str]

class TransformationRequest(BaseModel):
    data: Dict[str, Any]
    mapping: Dict[str, str]
    array_path: Optional[str] = Field(None, description="Dot notation path to array if transforming array items")
    preserve_null: bool = Field(default=False, description="If true, preserve null values in the output")

app = FastAPI(title="Data Processing API")

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
    collection = request.collection[0] if request.collection else []
    keys_to_remove = request.keysToRemove
    
    for item in collection:
        for key in keys_to_remove:
            if key in item:
                del item[key]
    
    return [collection]

@app.post("/transform")
def transform_data(request: TransformationRequest):
    """Transform JSON data based on a mapping configuration.
    
    Features:
    - Supports nested object traversal using dot notation
    - Can transform entire arrays of objects
    - Preserves null values if requested
    - Handles missing keys gracefully
    """
    try:
        def get_nested_value(obj: Union[Dict, List], path: str) -> Any:
            """Get value from nested dictionary or list using dot notation.
            Handles array indices and nested objects."""
            if not path:
                return None

            keys = path.split('.')
            current = obj

            for key in keys:
                # Handle array index if key is numeric
                if isinstance(current, list) and key.isdigit():
                    index = int(key)
                    if 0 <= index < len(current):
                        current = current[index]
                    else:
                        return None
                # Handle dictionary access
                elif isinstance(current, dict):
                    current = current.get(key)
                    if current is None:
                        return None
                else:
                    return None

            return current

        # If we're transforming array items
        if request.array_path:
            source_array = get_nested_value(request.data, request.array_path)
            
            if not isinstance(source_array, list):
                raise HTTPException(
                    status_code=400,
                    detail=f"Array path '{request.array_path}' does not point to a list"
                )
            
            transformed_array = []
            for item in source_array:
                transformed_item = {}
                for new_key, source_path in request.mapping.items():
                    value = get_nested_value(item, source_path)
                    if value is not None or request.preserve_null:
                        transformed_item[new_key] = value
                if transformed_item:  # Only add non-empty items
                    transformed_array.append(transformed_item)
            
            return {
                "transformed_data": transformed_array,
                "items_processed": len(source_array),
                "items_transformed": len(transformed_array)
            }
        
        # Regular transformation for single object
        result = {}
        for new_key, source_path in request.mapping.items():
            value = get_nested_value(request.data, source_path)
            if value is not None or request.preserve_null:
                result[new_key] = value
        
        return {
            "transformed_data": result,
            "fields_mapped": len(result)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Transformation failed: {str(e)}"
        )

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8001)
