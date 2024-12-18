#!/bin/bash

echo "Testing API endpoints..."
echo

echo "1. Testing Sentiment Analysis:"
curl -s "http://localhost:8001/sentiment-analysis/This%20is%20a%20great%20day!" | json_pp
echo -e "\n"

echo "2. Testing Remove Keys:"
curl -s -X POST "http://localhost:8001/keys/remove" \
-H "Content-Type: application/json" \
-d '{
  "collection": [[
    {"id": 1, "name": "John", "age": 30, "extra": "remove_me"},
    {"id": 2, "name": "Jane", "age": 25, "extra": "remove_me"}
  ]],
  "keysToRemove": ["extra", "age"]
}' | json_pp
echo -e "\n"

echo "3. Testing Transform Data:"
curl -s -X POST "http://localhost:8001/transform" \
-H "Content-Type: application/json" \
-d '{
  "data": {
    "user": {
      "personal": {
        "firstName": "John",
        "lastName": "Doe"
      },
      "contact": {
        "email": "john@example.com"
      }
    }
  },
  "mapping": {
    "name": "user.personal.firstName",
    "email": "user.contact.email"
  }
}' | json_pp
echo -e "\n"

echo "4. Testing Text Statistics:"
curl -s -X POST "http://localhost:8001/text-stats/analyze" \
-H "Content-Type: application/json" \
-d '{
  "text": "This is a sample text. It contains multiple sentences and some repeated words. This text will be analyzed.",
  "include_word_freq": true
}' | json_pp 