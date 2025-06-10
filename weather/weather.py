from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Initialize OpenAI client
openai_client = openai.AsyncOpenAI(api_key=os.getenv("OPEN_API_KEY"))

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

@mcp.tool()
async def unhinged_coach(message: str) -> str:
    """Get unhinged coaching advice from an AI coach with a motivational image.

    Args:
        message: The message or question to ask the unhinged coach
    """
    try:
        # Generate both coaching text and image prompt in parallel for speed
        import asyncio
        
        # Task 1: Generate the coaching text
        coaching_task = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an unhinged, chaotic and over-the-top motivational coach. Be extremely enthusiastic, use CAPS frequently but not all the time, sprinkle those emojis, and give advice that's motivational but completely over the top and dramatic. Be encouraging but in the most intense way possible. Make your responses entertaining and fun while still being helpful. Keep it short, maximum 300 characters. Use emojis to enhance the message! 🎉🔥💪"
                },
                {"role": "user", "content": message}
            ],
            max_tokens=300,
            temperature=0.9
        )
        
        # Task 2: Generate a creative image prompt
        image_prompt_task = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a chaotic meme creator! Create WILD and RIDICULOUS image prompts for motivational memes. Be creative, absurd, and over-the-top! Include random elements like: animals doing workouts, food metaphors, superhero themes, weird scenarios, pop culture references, dramatic weather, or anything UNHINGED! Keep it under 100 words but make it EPIC! 🎨🔥"
                },
                {"role": "user", "content": f"Create a meme image prompt for someone who says: '{message}'"}
            ],
            max_tokens=150,
            temperature=1.0
        )
        
        # Wait for both tasks to complete
        chat_response, prompt_response = await asyncio.gather(coaching_task, image_prompt_task)
        
        coaching_text = chat_response.choices[0].message.content
        creative_image_prompt = prompt_response.choices[0].message.content
        
        # Generate the image with the creative prompt (smaller size for speed)
        image_response = await openai_client.images.generate(
            model="dall-e-3",
            prompt=creative_image_prompt,
            size="1024x1024",  # Smaller for faster generation
            quality="standard",
            n=1
        )
        
        image_url = image_response.data[0].url
        
        # Combine text and image
        return f"{coaching_text}\n\n ![]({image_url})"
        
    except Exception as e:
        return f"ERROR: The coach is having a breakdown! {str(e)}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
