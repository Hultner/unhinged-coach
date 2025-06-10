from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os
from pathlib import Path

# Import the unhinged_coach function from the weather module
from weather import unhinged_coach

app = FastAPI(
    title="Unhinged Coach API",
    description="An AI-powered unhinged motivational coach with image generation",
    version="1.0.0"
)

class CoachRequest(BaseModel):
    message: str

class CoachResponse(BaseModel):
    response: str

class CallRequest(BaseModel):
    inputs: dict

class CallResponse(BaseModel):
    output: str

@app.get("/.well-known/ai-plugin.json")
async def ai_plugin_manifest():
    """AI plugin manifest endpoint."""
    return {
        "schema_version": "v1",
        "name_for_human": "Unhinged Coach",
        "name_for_model": "unhinged_coach",
        "description_for_human": "Get over-the-top motivational coaching advice with AI-generated meme images",
        "description_for_model": "A chaotic and enthusiastic motivational coach that provides extreme motivational advice with custom AI-generated meme images. Perfect for when you need motivation that's completely unhinged and entertaining.",
        "auth": {
            "type": "none"
        },
        "api": {
            "type": "openapi",
            "url": "/openapi.json"
        },
        "logo_url": "https://example.com/logo.png",
        "contact_email": "support@unhingedcoach.com",
        "legal_info_url": "https://example.com/legal"
    }

@app.post("/call")
async def call_endpoint(request: CallRequest):
    """Main call endpoint that accepts inputs and returns coach response."""
    try:
        # Extract message from inputs
        message = request.inputs.get("message", "")
        if not message:
            raise HTTPException(status_code=400, detail="Message is required in inputs")
        
        # Get response from unhinged coach
        coach_response = await unhinged_coach(message)
        
        return CallResponse(output=coach_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Coach breakdown: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the Unhinged Coach API! 🔥💪",
        "endpoints": {
            "/.well-known/ai-plugin.json": "GET - AI plugin manifest",
            "/call": "POST - Main endpoint for getting coach advice",
            "/coach": "POST - Alternative endpoint for getting coach advice",
            "/docs": "GET - Interactive API documentation",
            "/health": "GET - Health check"
        }
    }

@app.post("/coach", response_model=CoachResponse)
async def get_coaching(request: CoachRequest):
    """Get unhinged motivational coaching advice with an AI-generated meme image.
    
    Args:
        request: CoachRequest containing the message to ask the coach
        
    Returns:
        CoachResponse with the coach's advice and image
    """
    try:
        response = await unhinged_coach(request.message)
        return CoachResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Coach breakdown: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "The coach is ready to MOTIVATE! 🎯🔥"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)