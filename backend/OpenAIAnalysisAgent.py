import openai

class OpenAIAnalysisAgent:
    def __init__(self, api_key):
        openai.api_key = api_key

    def analyze(self, text, url, pdf_text): #method to analyze the given text, urls and PDF. Text and PDF are shortend with a slice, to not exceed the token maximum
        prompt = f"""Analysiere die Inhalte von {url} und dem PDF (falls vorhanden) und entwickle daraus ein Geschäftsmodell mit 2 - 3 detaillierten Aspekten.
                Website-Inhalt: {text[:3000]}, PDF-Inhalt: {pdf_text[:2000]}"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def revise_with_feedback(self, analysis, feedback):
        prompt = f"""Nutze das folgende Feedback, um die Analyse zu verbessern:
        Feedback: {feedback}, Originalanalyse: {analysis}
        """

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def analyzeText(self, text): #method to analyze the given text, urls and PDF. Text and PDF are shortend with a slice, to not exceed the token maximum
        prompt = f"""Analysiere die Inhalte dieses Textes und entwickle daraus ein Geschäftsmodell.
                Text-Inhalt: {text[:3000]}"""

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()