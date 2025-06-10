#!/bin/bash

# Test script for Unhinged Coach API using curl
# Make sure the server is running: python api_server.py

BASE_URL="http://localhost:8000"

echo "=== Testing Unhinged Coach API with curl ==="
echo

echo "1. Testing AI Plugin Manifest:"
echo "GET /.well-known/ai-plugin.json"
curl -s "$BASE_URL/.well-known/ai-plugin.json" | jq .
echo
echo

echo "2. Testing Call Endpoint:"
echo "POST /call"
curl -s -X POST "$BASE_URL/call" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {
      "message": "I need motivation to exercise!"
    }
  }' | jq .
echo
echo

echo "3. Testing Health Check:"
echo "GET /health"
curl -s "$BASE_URL/health" | jq .
echo
echo

echo "4. Testing Root Endpoint:"
echo "GET /"
curl -s "$BASE_URL/" | jq .
echo
echo

echo "=== Tests Complete ==="
