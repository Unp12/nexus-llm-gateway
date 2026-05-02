import httpx
from app.core.config import settings

async def call_openai(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini", 
        "messages": [{"role": "user", "content": prompt}]
    }
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(settings.OPENAI_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]