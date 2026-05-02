from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.router import resilient_llm_call

app = FastAPI(title="Nexus LLM Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str
    provider: str = "gemini"

@app.post("/api/v1/generate")
async def generate_response(request: GenerateRequest):
    try:
        result = await resilient_llm_call(request.prompt, request.provider)
        return result
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))