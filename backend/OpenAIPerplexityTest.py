from PerplexityAgent import PerplexityAgent
from config import OPENAI_API_KEY, PERPLEXITY_API_KEY
from OpenAIAnalysisAgent import OpenAIAnalysisAgent
from OpenAIReviewerAgent import OpenAIReviewerAgent
#from WebScraper import WebScraper

def main():
    analysisAgent = OpenAIAnalysisAgent(OPENAI_API_KEY)
    reviewerAgent = OpenAIReviewerAgent(OPENAI_API_KEY)
    perplexityAgent = PerplexityAgent()
   #scraper = WebScraper()

    url = ""
    pdf_text = ""

    #Perplexity Textanalyse:
    perplexityText = perplexityAgent.extractData(PERPLEXITY_API_KEY)

    score = 0
    count = 0
    satisfied = False

    analysis = analysisAgent.analyzeText(perplexityText)
    print(analysis)

    while not satisfied and score < 7 and count < 4:
        review = reviewerAgent.review_analysis(analysis)
        print(review)
        score = reviewerAgent.extract_score(review)
        count = count + 1
        if score < 7:
            review2 = analysisAgent.revise_with_feedback(analysis, review)
            print(review2)

if __name__ == "__main__":
    main()
