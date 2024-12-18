from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import sentiment, transform, keys

app = FastAPI(
    title="Data Processing API",
    description="API for data transformation, sentiment analysis, and key management",
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
async def root():
    return RedirectResponse(url="/docs")

# Health check endpoint
@app.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(sentiment.router, tags=["sentiment"])
app.include_router(transform.router, tags=["transform"])
app.include_router(keys.router, tags=["keys"])

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
    }
]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True) 