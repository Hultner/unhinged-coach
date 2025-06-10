#!/usr/bin/env python3
"""
Test script for the Unhinged Coach API endpoints.
"""
import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"

async def test_api_endpoints():
    """Test all API endpoints."""
    async with httpx.AsyncClient() as client:
        print("Testing Unhinged Coach API Endpoints")
        print("=" * 50)
        
        # Test 1: AI Plugin Manifest
        print("\n1. Testing /.well-known/ai-plugin.json")
        try:
            response = await client.get(f"{BASE_URL}/.well-known/ai-plugin.json")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                manifest = response.json()
                print(f"Plugin Name: {manifest.get('name_for_human')}")
                print(f"Description: {manifest.get('description_for_human')}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test 2: Call Endpoint
        print("\n2. Testing /call endpoint")
        try:
            test_payload = {
                "inputs": {
                    "message": "I need motivation to finish my project!"
                }
            }
            response = await client.post(
                f"{BASE_URL}/call",
                json=test_payload,
                timeout=60.0  # Longer timeout for AI generation
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                output = result.get('output', '')
                print(f"Output length: {len(output)} characters")
                print(f"Contains image: {'![](' in output}")
                print(f"First 200 chars: {output[:200]}...")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test 3: Health Check
        print("\n3. Testing /health endpoint")
        try:
            response = await client.get(f"{BASE_URL}/health")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                health = response.json()
                print(f"Health: {health}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test 4: Root endpoint
        print("\n4. Testing / (root) endpoint")
        try:
            response = await client.get(f"{BASE_URL}/")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                root = response.json()
                print(f"Available endpoints: {list(root.get('endpoints', {}).keys())}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("Make sure the API server is running on localhost:8000")
    print("Start it with: python api_server.py")
    print("\nPress Enter to continue with tests...")
    input()
    
    asyncio.run(test_api_endpoints())
