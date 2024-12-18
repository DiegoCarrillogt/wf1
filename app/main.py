from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routers import sentiment, transform, keys, text_stats

app = FastAPI(
    title="Data Processing API",
    description="API for data transformation, sentiment analysis, and text analysis",
    version="1.0.0"
)

# Redirect root to docs
@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs", status_code=308)

# Include routers
app.include_router(sentiment.router)
app.include_router(transform.router)
app.include_router(keys.router)
app.include_router(text_stats.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True) 