from fastapi import APIRouter
from pydantic import BaseModel
from backend.PerplexityAgent import PerplexityAgent
from backend.config import PERPLEXITY_API_KEY

router = APIRouter(prefix="/perplexity", tags=["Perplexity Agent"])

agent = PerplexityAgent()

class PromptRequest(BaseModel):
    prompt_text: str

@router.post("/extract")
def extract_info(request: PromptRequest):
    result = agent.extract_data(api_key=PERPLEXITY_API_KEY, prompt_text=request.prompt_text)
    return result
