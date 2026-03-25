import os
import asyncio
import logging
from google.adk.agents import Agent
from google.adk import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class GeminiAgent:
    """
    Summarization Agent using the Google Agent Development Kit (ADK).
    This structure is ADK-friendly and production-ready.
    """
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        # 1. Define the ADK Agent
        self.agent = Agent(
            name="TextSummarizer",
            model="gemini-flash-latest", # Reliable model
            instruction=(
                "You are a professional editor. Distill the input text into a highly concise "
                "3-line summary focusing only on the most essential facts. Output as a single paragraph."
            )
        )
        
        # 2. Setup the Runner (ADK requires a session service)
        self.runner = Runner(
            app_name="SummarizerApp",
            agent=self.agent,
            session_service=InMemorySessionService(),
            auto_create_session=True
        )
        
        # Fallback models mapping if ADK/Main model fails
        self.fallback_models = [
            "gemini-flash-latest",
            "gemini-2.0-flash-lite",
            "gemini-2.0-flash",
            "gemini-1.5-pro"
        ]

    async def summarize(self, text: str):
        """
        Executes the summarization using the ADK Runner.
        """
        try:
            logger.info(f"ADK Runner attempting summarization with {self.agent.model}...")
            
            # ADK Runner uses run_async with a session and user_id
            full_summary = ""
            user_msg = types.Content(role="user", parts=[types.Part(text=text)])
            
            async for event in self.runner.run_async(
                user_id="default_user",
                session_id="summarization_session",
                new_message=user_msg
            ):
                # Collector logic for ADK events
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            full_summary += part.text
            
            if full_summary:
                return {
                    "summary": full_summary.strip(),
                    "model": self.agent.model
                }
            else:
                raise Exception("ADK Runner returned empty response.")
                
        except Exception as e:
            logger.warning(f"ADK Runner failed: {e}. Attempting direct fallback...")
            return await self._fallback_summarize(text)

    async def _fallback_summarize(self, text: str):
        """
        Direct fallback for quota issues using the provided list.
        """
        from google import genai
        client = genai.Client(api_key=self.api_key)
        
        for model_name in self.fallback_models:
            try:
                logger.info(f"Fallback attempting model: {model_name}")
                prompt = (
                    "SYSTEM: You are a professional editor. Distill the following text into a highly concise "
                    "3-line summary. focus ONLY on the core objective and most essential facts. "
                    "Provide the result as one cohesive paragraph. Output ONLY the summary text.\n\n"
                    f"TEXT TO SUMMARIZE:\n{text}"
                )
                
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response.text:
                    return {
                        "summary": response.text.strip(),
                        "model": model_name
                    }
            except Exception:
                continue
        
        raise Exception("All models and ADK failover exhausted.")
