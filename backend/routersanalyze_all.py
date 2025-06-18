from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from backend.OpenAIAnalysisAgent import OpenAIAnalysisAgent
from backend.OpenAIReviewerAgent import OpenAIReviewerAgent
from backend.pdfReader import extract_text_from_pdf
from backend.WebScraper import scrape_website

router = APIRouter()

class AnalyzeRequest(BaseModel):
    urls: Optional[List[str]] = []
    prompt: Optional[str] = ""
    max_feedback_loops: Optional[int] = 3

class AnalyzeResponse(BaseModel):
    final_analysis: str
    score: int
    feedback_iterations: List[str]

@router.post("/analyze-all", response_model=AnalyzeResponse)
async def analyze_all(
    request: AnalyzeRequest,
    pdf_files: Optional[List[UploadFile]] = File(None)
):
    pdf_texts = []
    if pdf_files:
        for pdf in pdf_files:
            content = await pdf.read()
            pdf_texts.append(extract_text_from_pdf(content))

    web_texts = []
    for url in request.urls:
        try:
            text = scrape_website(url)
            web_texts.append(text)
        except Exception as e:
            web_texts.append(f"[Fehler beim Scrapen von {url}: {str(e)}]")

    full_text = "\n\n".join([request.prompt] + pdf_texts + web_texts)

    analyzer = OpenAIAnalysisAgent()
    reviewer = OpenAIReviewerAgent()

    feedback_iterations = []
    for i in range(request.max_feedback_loops):
        analysis = analyzer.analyze(full_text)
        feedback, score = reviewer.review(analysis)
        feedback_iterations.append(
            f"[Durchgang {i+1}]\nAnalyse: {analysis}\nFeedback: {feedback}\nScore: {score}"
        )
        if score >= 8:
            break
        full_text += "\n\n" + feedback

    return AnalyzeResponse(
        final_analysis=analysis,
        score=score,
        feedback_iterations=feedback_iterations
    )
