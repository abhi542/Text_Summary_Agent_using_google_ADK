import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .agent import GeminiAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI & Agent
app = FastAPI(title="ADK Summarization Agent")
agent = GeminiAgent()

class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str
    model: str

@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ADK Summarization Agent"}

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    """
    API endpoint for text summarization.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty")

    try:
        result = agent.summarize(request.text)
        return SummarizeResponse(**result)
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            raise HTTPException(status_code=429, detail="API Quota Exceeded. Please try again later.")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {error_msg}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
