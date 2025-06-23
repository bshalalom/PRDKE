from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
import requests

from backend.PerplexityAgent import PerplexityAgent
from backend.OpenAIAnalysisAgent import OpenAIAnalysisAgent
from backend.OpenAIReviewerAgent import OpenAIReviewerAgent
from backend.pdfReader import extract_text_from_pdf
# WICHTIG: Wir importieren die jetzt asynchrone scrape_website Funktion
from backend.WebScraper import scrape_website, ScrapedContent
import backend.config as config

router = APIRouter()

class AnalyzeResponse(BaseModel):
    final_analysis: str
    urls_used: List[str]
    feedback_iterations: List[str]
    score: int

# Die Hauptfunktion ist bereits 'async def', was perfekt ist
@router.post("/analyze-all", response_model=AnalyzeResponse)
async def analyze_all(
    prompt: str = Form(""),
    max_feedback_loops: int = Form(3),
    manual_pdf_files: Optional[List[UploadFile]] = File(None, alias="pdf_files")
):
    print("Starte die Perplexity-Suche für den Prompt...")
    perplexity_agent = PerplexityAgent()
    perplexity_result = perplexity_agent.extract_data(api_key=config.PERPLEXITY_API_KEY, prompt_text=prompt)
    found_urls = perplexity_result.get("citations", [])
    print(f"Perplexity hat {len(found_urls)} URLs gefunden: {found_urls}")
    
    pdf_texts_list = []
    if manual_pdf_files:
        for pdf in manual_pdf_files:
            content = await pdf.read()
            pdf_pages = extract_text_from_pdf(content)
            pdf_texts_list.append("\n".join(pdf_pages))

    web_texts = []
    for url in found_urls:
        try:
            if url.lower().endswith('.pdf'):
                print(f"Verarbeite URL als PDF: {url}")
                response = requests.get(url, timeout=20)
                response.raise_for_status()
                pdf_pages = extract_text_from_pdf(response.content)
                pdf_texts_list.append("\n".join(pdf_pages))
            else:
                print(f"Verarbeite URL als Webseite: {url}")
                # KORREKTUR: Wir verwenden 'await', um die asynchrone Funktion aufzurufen
                scraped_data = await scrape_website(url)
                if scraped_data.text and not scraped_data.error:
                    web_texts.append(scraped_data.text)
                elif scraped_data.error:
                     web_texts.append(f"[Fehler beim Scrapen von {url}: {scraped_data.error}]")
        except Exception as e:
            error_message = f"[Fehler bei der Verarbeitung von URL {url}: {str(e)}]"
            print(error_message)
            web_texts.append(error_message)

    combined_pdf_text = "\n\n".join(pdf_texts_list)
    full_text = "\n\n".join([prompt] + pdf_texts_list + web_texts)

    analyzer = OpenAIAnalysisAgent(api_key=config.OPENAI_API_KEY)
    reviewer = OpenAIReviewerAgent(api_key=config.OPENAI_API_KEY)

    feedback_iterations = []
    analysis = "Keine Analyse durchgeführt."
    score = 0
    for i in range(max_feedback_loops):
        analysis = analyzer.analyze(full_text, pdf_text=combined_pdf_text)
        feedback = reviewer.review_analysis(analysis)
        score = reviewer.extract_score(feedback)
        feedback_iterations.append(
            f"[Durchgang {i+1}]\nAnalyse: {analysis}\nFeedback: {feedback}\nScore: {score}"
        )
        if score >= 8:
            break
        full_text += "\n\n" + feedback

    return AnalyzeResponse(
        final_analysis=analysis,
        urls_used=found_urls,
        feedback_iterations=feedback_iterations,
        score=score
    )