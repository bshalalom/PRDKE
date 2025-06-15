import openai
import requests
import json

from backend.WebScraper import WebScraper


class PerplexityAgent:
    def __init__(self):
        pass

    def extract_data(self, api_key, prompt_text):
        webscraper = WebScraper()
        url = "https://api.perplexity.ai/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "sonar",
            "search": True,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        prompt_text
                       # "Bitte gib mir aktuelle Informationen zur wirtschaftlichen Entwicklung und zum Produktportfolio der Voest aus dem Jahr 2024 oder 2025"
                    )
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()

            # Textinhalt der Antwort
            print("🔹 Antwort von Perplexity:\n")
            print(result["choices"][0]["message"]["content"])

            # Citations ausgeben (Quellen)
            print("\n🔹 Quellen (aus 'citations'):")
            citations = result.get("citations", [])
            if citations:
                for citation in citations:
                    print(f"- {citation}")
            else:
                print("⚠️ Keine Quellen im Feld 'citations' enthalten.")

            # Optional: Rohdaten anzeigen (zum Debuggen)
            # print(json.dumps(result, indent=2)[:2000])  # kürze bei Bedarf

            #!!!!!Rückgabe nur von Text für Testzwecke!!!!!
            content = result["choices"][0]["message"]["content"]
            return {"content": content, "citations": citations}     #return both content and citations, for easier further processing
        else:
            print("❌ Fehler:", response.status_code)
            print(response.text)

