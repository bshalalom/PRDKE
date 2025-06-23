import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

#Beautiful Soup not compatible
#class WebScraper:
#    def __init__(self):
#        self.session = HTMLSession()

#    def scrapeWebsite(self, url):
#       try:
#          response = requests.get(url)
#         response.raise_for_status()
#        html = response.text
#       bs = BeautifulSoup(html, 'html.parser')
#      text = bs.get_text()
#     return text
#except Exception as e:
#   print("Fehler beim Scrapen von {url}: {e}")
#  return ""


from requests_html import AsyncHTMLSession
from pydantic import BaseModel, Field
from typing import Optional

class ScrapedContent(BaseModel):
    url: str
    text: Optional[str] = None
    error: Optional[str] = None

class WebScraper:
    """
    Eine Klasse zum Scrapen von Webseiten-Inhalten, die von anderen Agenten verwendet werden kann.
    """
    def __init__(self):
        # Initialisierung kann hier erfolgen, falls notwendig
        pass

    async def scrape(self, url: str) -> ScrapedContent:
        """
        Asynchrone Methode zum Scrapen einer einzelnen URL.
        """
        session = AsyncHTMLSession()
        try:
            print(f"Versuche, die URL zu scrapen: {url}")
            response = await session.get(url, timeout=20)
            response.raise_for_status()
            await response.html.arender(timeout=20)
            body_text = response.html.find('body', first=True)
            if body_text:
                return ScrapedContent(url=url, text=body_text.text)
            else:
                return ScrapedContent(url=url, error="Konnte den Body-Inhalt der Seite nicht finden.")
        except Exception as e:
            return ScrapedContent(url=url, error=f"Fehler beim Scrapen von {url}: {e}")
        finally:
            await session.close()

# Eine eigenständige Funktion, die für Kompatibilität sorgt
async def scrape_website(url: str) -> ScrapedContent:
    """
    Eigenständige Funktion, die die WebScraper-Klasse nutzt.
    """
    scraper = WebScraper()
    return await scraper.scrape(url)