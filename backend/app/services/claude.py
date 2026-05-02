import httpx
from app.core.config import settings

async def call_claude(prompt: str) -> str:
    headers = {
        "x-api-key": settings.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["content"][0]["text"]