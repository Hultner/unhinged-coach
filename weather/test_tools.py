#!/usr/bin/env python3
"""
Test script to verify all MCP tools work correctly.
"""
import asyncio
import os
from weather import get_alerts, get_forecast, unhinged_coach

async def test_tools():
    print("Testing MCP Weather Tools")
    print("=" * 40)
    
    # Test weather alerts
    print("\n1. Testing get_alerts tool (CA):")
    try:
        alerts = await get_alerts("CA")
        print(f"Alerts result: {alerts[:200]}..." if len(alerts) > 200 else alerts)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test weather forecast
    print("\n2. Testing get_forecast tool (San Francisco):")
    try:
        forecast = await get_forecast(37.7749, -122.4194)  # San Francisco coords
        print(f"Forecast result: {forecast[:300]}..." if len(forecast) > 300 else forecast)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test unhinged coach
    print("\n3. Testing unhinged_coach tool:")
    try:
        coach_response = await unhinged_coach("I need motivation to finish my coding project!")
        print(f"Coach says: {coach_response}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 40)
    print("Testing complete!")

if __name__ == "__main__":
    asyncio.run(test_tools())
