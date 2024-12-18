# Data Processing API

A FastAPI-based REST API for data processing, text analysis, and data transformation.

## Features

- **Data Transformation**: Transform JSON data based on mapping configurations
- **Key Management**: Add or remove keys from data collections
- **Text Analysis**: 
  - Sentiment analysis
  - Text statistics (word count, readability, etc.)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <project-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the server:
```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

The API will be available at: http://localhost:8001
API documentation: http://localhost:8001/docs

## API Endpoints

### 1. Key Management

#### Remove Keys
```bash
POST /keys/remove
{
    "collection": [[
        {"id": 1, "name": "John", "age": 30},
        {"id": 2, "name": "Jane", "age": 25}
    ]],
    "keysToRemove": ["age"]
}
```

### 2. Data Transformation

#### Transform Data
```bash
POST /transform
{
    "data": {
        "user": {
            "personal": {
                "firstName": "John"
            }
        }
    },
    "mapping": {
        "name": "user.personal.firstName"
    }
}
```

### 3. Text Analysis

#### Sentiment Analysis
```bash
GET /sentiment-analysis/{text}
```

#### Text Statistics
```bash
POST /text-stats/analyze
{
    "text": "Your text here",
    "include_word_freq": true
}
```

## Project Structure

```
app/
├── main.py              # Main application file
├── models/             # Data models
│   └── schemas.py
├── routers/            # Route handlers
│   ├── sentiment.py
│   ├── transform.py
│   ├── text_stats.py
│   └── keys.py
└── services/           # Business logic
    ├── sentiment_service.py
    ├── transform_service.py
    ├── text_stats_service.py
    └── key_service.py
```

## Dependencies

- FastAPI
- Uvicorn
- TextBlob
- Pydantic

## Development

To add new features:
1. Add models in `app/models/schemas.py`
2. Create service logic in `app/services/`
3. Add routes in `app/routers/`
4. Include new routers in `main.py`
