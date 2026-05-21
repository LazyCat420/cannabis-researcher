import asyncio
import sys
import os
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.scraper_client import ScraperClient

async def main():
    client = ScraperClient(base_url="http://10.0.0.16:8001")
    url = "https://www.thcfarmer.com/threads/jack-herer.174402/"
    
    print("Fetching via scraper-service...")
    res = await client.scrape(url, engine="playwright", options={"raw_html": True})
    
    if not res.get("success"):
        print("Failed to fetch page:", res.get("error"))
        await client.close()
        return
        
    html = res.get("content")
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("article", class_="message")
    print("Found articles count:", len(articles))
    for i, art in enumerate(articles[:2]):
        print(f"\n--- Article {i+1} ---")
        # Let's print all image tags in this article
        imgs = art.find_all("img")
        print("Images found:")
        for img in imgs:
            print("  src:", img.get("src"), "data-url:", img.get("data-url"), "class:", img.get("class"))
            
        body = art.find(class_="message-body")
        if body:
            print("Message body sample:")
            print(body.get_text(separator=" ", strip=True)[:300])

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
