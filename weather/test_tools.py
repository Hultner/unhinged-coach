#!/usr/bin/env python3
"""
Test script to verify all MCP tools work correctly.
"""
import asyncio
import os
from weather import get_alerts, get_forecast, unhinged_coach

async def test_tools():
    print("Testing MCP Tools")
    print("=" * 40)
    
    # # Test weather alerts
    # print("\n1. Testing get_alerts tool (CA):")
    # try:
    #     alerts = await get_alerts("CA")
    #     print(f"Alerts result: {alerts[:200]}..." if len(alerts) > 200 else alerts)
    # except Exception as e:
    #     print(f"Error: {e}")
    
    # # Test weather forecast
    # print("\n2. Testing get_forecast tool (San Francisco):")
    # try:
    #     forecast = await get_forecast(37.7749, -122.4194)  # San Francisco coords
    #     print(f"Forecast result: {forecast[:300]}..." 
    # except Exception as e:
    #     print(f"Error: {e}")
    
    # Test unhinged coach
    # print("\n3. Testing unhinged_coach tool:")
    # try:
    #     coach_response = await unhinged_coach("I need motivation to finish my coding project!")
    #     print(f"Coach says: {coach_response}")
    # except Exception as e:
    #     print(f"Error: {e}")
    
    workout = """
Left abductor still hurt, was going to do a last max effort workout this week before my long break (hike), but will probably have to skip that so I can focus on recovery before the hike. 
Flat dumbbell press heavy
Right tricep still hurts so trying even lower weight this week (45->40kg), last try before the hike. Should normally comfortably do about 8-10 reps at 40kg. 
5 x 25kg (warm-up)
3 x 40kg (regular), Was feeling bad in right tricep after 3:ed rep so stayed there
Flat dumbbell press backoff
Dropping backoffs back by an additional 5kg as well. 
7 x 32.5kg (regular)
Dumbbell romainain deadlift
11 x 42.5kg (regular)
10 x 42.5kg (regular)
Lat pulldown
13 x 100kg (regular)
13 x 100kg (regular)
Dumbbell step up
Low weight, focus on recovery/rehab
15 x 15kg (regular)
Overhead cable tricep extension
5 x 25kg (warm-up)
15 x 40kg (drop-set)
  - 8 x 28.75kg (drop-set)
  - 7 x 21.25kg (drop-set)
  - 8 x 15kg (drop-set)
  - 7 x 10kg (drop-set)
Leg press toe-press
5 x 160kg (warm-up)
14 x 210kg (drop-set)
  - 9 x 170kg (drop-set)
  - 12 x 120kg (drop-set)
  - 10 x 90kg (drop-set)
  - 9 x 70kg (drop-set)
Machine lateral raise
5 x 5kg (warm-up)
15 x 7.5kg (drop-set)
  - 18 x 5kg (drop-set)
  - 16 x 2.5kg (drop-set)
Machine chest fly
5 x 10kg (warm-up)
10 x 15kg (regular)"""
    print("\n4. Testing unhinged_coach tool:")
    try:
        coach_response = await unhinged_coach(workout)
        print(f"Coach says: {coach_response}")
    except Exception as e:
        print(f"Error: {e}")
    print("\n" + "=" * 40)
    print("Testing complete!")

if __name__ == "__main__":
    asyncio.run(test_tools())
