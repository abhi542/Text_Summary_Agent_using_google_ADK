import os
import logging
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class GeminiAgent:
    """
    Modular AI Agent for text summarization with multi-model fallback.
    """
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.error("GEMINI_API_KEY not found in environment.")
        
        self.client = genai.Client(api_key=self.api_key)
        
        # Primary and fallback models
        self.models_to_try = [
            os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite"),
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-2.0-flash",
            "gemini-flash-latest"
        ]

    def summarize(self, text: str):
        """
        Distill text into a concise 3-line summary using the best available model.
        """
        last_error = ""
        for model_name in self.models_to_try:
            try:
                logger.info(f"Agent attempting summarization with model: {model_name}")
                
                prompt = (
                    "SYSTEM: You are a professional editor. Distill the following text into a highly concise "
                    "3-line summary. focus ONLY on the core objective and most essential facts. "
                    "Provide the result as one cohesive paragraph. Output ONLY the summary text.\n\n"
                    f"TEXT TO SUMMARIZE:\n{text}"
                )

                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config={
                        "temperature": 0.5,
                        "top_p": 0.9,
                    }
                )
                
                if response.text:
                    return {
                        "summary": response.text.strip(),
                        "model": model_name
                    }
                
            except Exception as e:
                last_error = str(e)
                logger.warning(f"Agent fallback: Model {model_name} failed: {last_error}")
                if "429" in last_error or "404" in last_error or "quota" in last_error.lower():
                    continue
                else:
                    continue

        raise Exception(f"All models failed. Last error: {last_error}")
