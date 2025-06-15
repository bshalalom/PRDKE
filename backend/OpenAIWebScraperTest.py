from PerplexityAgent import PerplexityAgent
from WebScraper import WebScraper
from config import OPENAI_API_KEY, PERPLEXITY_API_KEY
from OpenAIAnalysisAgent import OpenAIAnalysisAgent
from OpenAIReviewerAgent import OpenAIReviewerAgent

def main():
    analysisAgent = OpenAIAnalysisAgent(OPENAI_API_KEY)
    reviewerAgent = OpenAIReviewerAgent(OPENAI_API_KEY)
    perplexityAgent = PerplexityAgent()
    webscraper = WebScraper()

    text = ""

    # Perplexity Zitationen auslesen:
    citations = perplexityAgent.extract_data(PERPLEXITY_API_KEY)

    for citation in citations:
      text = text + " " + webscraper.scrapeWebsite(citation)



if __name__ == "__main__":
    main()
