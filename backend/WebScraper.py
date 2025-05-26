import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self):
        self.session = HTMLSession()

    def scrapeWebsite(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            html = response.text
            bs = BeautifulSoup(html, 'html.parser')
            text = bs.get_text()
            return text
        except Exception as e:
            print("Fehler beim Scrapen von {url}: {e}")
            return ""
