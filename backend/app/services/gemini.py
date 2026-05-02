import httpx
from app.core.config import settings

async def call_gemini(prompt: str) -> str:
    # Constructing the URL with the key correctly
    url = f"{settings.GEMINI_URL}?key={settings.GEMINI_API_KEY}"
    
    # Standard payload structure for Gemini 1.5 Flash
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    # Using a 10-second timeout to prevent the 503 from taking too long
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.post(url, json=payload)
            
            # This will show us the exact error from Google if it fails
            if response.status_code != 200:
                print(f"Gemini API Error ({response.status_code}): {response.text}")
                response.raise_for_status()
                
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
            
        except Exception as e:
            print(f"Request Exception: {str(e)}")
            raise e