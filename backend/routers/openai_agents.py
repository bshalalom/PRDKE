from fastapi import APIRouter
from pydantic import BaseModel
from backend.OpenAIAnalysisAgent import OpenAIAnalysisAgent
from backend.OpenAIReviewerAgent import OpenAIReviewerAgent
from backend.config import OPENAI_API_KEY

#extra class for the openAI instances, for FastAPI usage
#pydantic for automatic data validation

router = APIRouter(prefix="/openai", tags=["OpenAI Agents"])
analysis_agent = OpenAIAnalysisAgent(OPENAI_API_KEY)
reviewer_agent = OpenAIReviewerAgent(OPENAI_API_KEY)

class AnalyzeRequest(BaseModel):
    text: str
    pdf_text: str ="" #can be empty if there is no PDF

class ReviseRequest(BaseModel):
    analysis: str
    feedback: str

class ReviewRequest(BaseModel):
    analysis: str

@router.post("/analyze")
def analyze(request: AnalyzeRequest):
    return {"analysis": analysis_agent.analyze(request.text, request.pdf_text)}

@router.post("/revise")
def revise(request: ReviseRequest):
    return {"revised_analysis": analysis_agent.revise_with_feedback(request.analysis, request.feedback)}

@router.post("/review")
def review(request: ReviewRequest):
    feedback = reviewer_agent.review_analysis(request.analysis)
    score = reviewer_agent.extract_score(feedback)
    return {"feedback": feedback, "score": score}
