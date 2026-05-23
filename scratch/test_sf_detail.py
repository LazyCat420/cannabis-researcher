import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.scraper_client import ScraperClient

async def main():
    s = ScraperClient()
    url = "https://seedfinder.eu/en/strain-info/Qrazy_Train/SubCools_The_Dank/"
    res = await s.scrape(url, engine="playwright", options={"raw_html": True})
    content = res.get("content", "") or ""
    print(f"Content length: {len(content)}")
    if "cloudflare" in content.lower():
        print("Scrape failed: cloudflare challenge detected")
    else:
        print("Scrape succeeded! Title search:")
        import re
        title = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
        if title:
            print(f"Title: {title.group(1)}")
            
    await s.close()

if __name__ == "__main__":
    asyncio.run(main())
