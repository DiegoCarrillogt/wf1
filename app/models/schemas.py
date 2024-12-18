from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

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

class TextStatsRequest(BaseModel):
    text: str = Field(..., description="The text to analyze")
    include_word_freq: bool = Field(default=True, description="Whether to include word frequency analysis")