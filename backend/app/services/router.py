import asyncio
import time
import httpx
from app.services.gemini import call_gemini
from app.services.openai import call_openai
from app.services.claude import call_claude

# Map provider strings to their functions
SERVICE_MAP = {
    "gemini": call_gemini,
    "openai": call_openai,
    "claude": call_claude
}

async def resilient_llm_call(prompt: str, primary: str = "gemini"):
    start_time = time.time()
    primary_func = SERVICE_MAP.get(primary, call_gemini)
    
    # Define a fallback (if primary is not OpenAI, use OpenAI as fallback, else Gemini)
    fallback_name = "openai" if primary != "openai" else "gemini"
    fallback_func = SERVICE_MAP[fallback_name]

    try:
        # 15-second hard timeout for the primary provider
        response = await asyncio.wait_for(primary_func(prompt), timeout=15.0)
        latency = round((time.time() - start_time) * 1000)
        return {"response": response, "provider_used": primary, "latency_ms": latency}

    except (httpx.TimeoutException, httpx.HTTPStatusError, asyncio.TimeoutError):
        # Primary failed, trigger fallback silently
        try:
            response = await asyncio.wait_for(fallback_func(prompt), timeout=15.0)
            latency = round((time.time() - start_time) * 1000)
            return {"response": response, "provider_used": fallback_name, "latency_ms": latency}
        except Exception as e:
            raise Exception("All LLM providers are currently unavailable.")