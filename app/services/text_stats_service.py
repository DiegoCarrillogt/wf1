from textblob import TextBlob
import re
from typing import List, Dict

def count_sentences(text: str) -> int:
    """Count the number of sentences in the text."""
    blob = TextBlob(text)
    return len(blob.sentences)

def count_words(text: str) -> int:
    """Count the number of words in the text."""
    words = re.findall(r'\w+', text.lower())
    return len(words)

def get_word_frequency(text: str, top_n: int = 5) -> Dict[str, int]:
    """Get the frequency of words in the text."""
    words = re.findall(r'\w+', text.lower())
    word_freq = {}
    for word in words:
        if len(word) > 2:  # Ignore very short words
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and get top N
    sorted_freq = dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n])
    return sorted_freq

def calculate_readability(text: str) -> float:
    """Calculate a simple readability score based on average sentence length."""
    blob = TextBlob(text)
    if not blob.sentences:
        return 0.0
    
    avg_sentence_length = sum(len(str(sentence).split()) for sentence in blob.sentences) / len(blob.sentences)
    # Simple readability score: higher means more complex
    return round(avg_sentence_length / 10, 2)

def analyze_text_stats(text: str, include_word_freq: bool = True) -> Dict:
    """Analyze text and return various statistics."""
    try:
        stats = {
            "text_length": len(text),
            "word_count": count_words(text),
            "sentence_count": count_sentences(text),
            "average_word_length": round(len(text) / max(count_words(text), 1), 2),
            "readability_score": calculate_readability(text),
        }
        
        if include_word_freq:
            stats["word_frequency"] = get_word_frequency(text)
            
        return stats
    except Exception as e:
        raise ValueError(f"Error analyzing text: {str(e)}") 