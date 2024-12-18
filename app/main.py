from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import sentiment, transform, keys, text_stats

app = FastAPI(
    title="Data Processing API",
    description="API for data transformation, sentiment analysis, text analysis, and key management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redirect root to docs
@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs", status_code=308)

# Include routers
app.include_router(sentiment.router, tags=["sentiment"])
app.include_router(transform.router, tags=["transform"])
app.include_router(keys.router, tags=["keys"])
app.include_router(text_stats.router, tags=["text-analysis"])

# Add OpenAPI tags metadata
app.openapi_tags = [
    {
        "name": "sentiment",
        "description": "Sentiment analysis operations"
    },
    {
        "name": "transform",
        "description": "Data transformation operations"
    },
    {
        "name": "keys",
        "description": "Key management operations"
    },
    {
        "name": "text-analysis",
        "description": "Text analysis and statistics operations"
    }
]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True) 