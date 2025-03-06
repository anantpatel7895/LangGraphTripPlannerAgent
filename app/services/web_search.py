import requests
from bs4 import BeautifulSoup
import os

class WebSearch:

    def __init__(self, engine="duckduckgo", api_key=None, cx=None):
        """
        Initialize the WebSearch class with a search engine and optional API keys.

        :param engine: Search engine to use ("duckduckgo", "google", "bing", "tavily").
        :param api_key: API key for Google, Bing, or Tavily (not needed for DuckDuckGo).
        :param cx: Custom Search Engine ID (only for Google Search API).
        """
        self.engine = engine.lower()
        self.api_key = api_key if api_key else os.getenv(f"{self.engine.upper()}_API_KEY")
        self.cx = cx if cx else os.getenv("cx")

    def search(self, query, max_results=5):
        """
        Perform a search using the selected search engine.

        :param query: The search query.
        :param max_results: Number of results to retrieve (default: 5).
        :return: A list of search results.
        """
        if self.engine == "duckduckgo":
            return self._search_duckduckgo(query, max_results)
        elif self.engine == "google" and self.api_key and self.cx:
            return self._search_google(query, max_results)
        elif self.engine == "bing" and self.api_key:
            return self._search_bing(query, max_results)
        elif self.engine == "tavily" and self.api_key:
            return self._search_tavily(query, max_results)
        else:
            raise ValueError("Invalid search engine or missing API credentials.")

    def _search_duckduckgo(self, query, max_results):
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
        response = requests.get(url).json()
        results = response.get("RelatedTopics", [])
        
        return [res["Text"] for res in results[:max_results] if "Text" in res]

    def _search_google(self, query, max_results):
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={self.api_key}&cx={self.cx}&num={max_results}"
        response = requests.get(url).json()

        # return response
        return [{"title":item["title"],  "url":item["link"], "content":item["snippet"]} for item in response.get("items", [])]

    def _search_bing(self, query, max_results):
        url = f"https://api.bing.microsoft.com/v7.0/search?q={query}&count={max_results}"
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        response = requests.get(url, headers=headers).json()
        return [item["name"] + " - " + item["url"] for item in response.get("webPages", {}).get("value", [])]

    def _search_tavily(self, query, max_results):
        url = "https://api.tavily.com/search"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"query": query, "num_results": max_results}
        response = requests.post(url, headers=headers, json=params).json()
        return response
        # return [item["title"] + " - " + item["url"] for item in response.get("results", [])]

    def scrape_webpage(self, url):
        """
        Scrape the given webpage and extract clean text content in a structured format.

        :param url: The URL of the webpage to scrape.
        :return: A dictionary containing the title, headers, and paragraphs of the page.
        """
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract page title
        title = soup.title.string if soup.title else "No Title"

        # Extract all headings
        headers = [h.get_text().strip() for h in soup.find_all(["h1", "h2", "h3"])]

        # Extract all text from paragraphs
        paragraphs = [p.get_text().strip() for p in soup.find_all("p")]

        return {
            "title": title,
            "headers": headers,
            "content": "\n".join(paragraphs)
        }

# Example usage:
# searcher = WebSearch(engine="google", api_key="your_google_api_key", cx="your_google_cx")
# results = searcher.search("Latest AI advancements")
# print(results)
# page_data = searcher.scrape_webpage(results[0].split(" - ")[-1])
# print(page_data)