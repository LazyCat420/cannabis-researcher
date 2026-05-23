import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../scraper-service")))

from app.engines.crawl4ai_engine import Crawl4aiEngine

async def main():
    engine = Crawl4aiEngine()
    url = "https://seedfinder.eu/en/strain-info/Qrazy_Train/SubCools_The_Dank/"
    print(f"Fetching {url} using crawl4ai...")
    res = await engine.fetch(url, {})
    print(f"Success: {res.success}")
    print(f"Error: {res.error}")
    content = res.content or ""
    print(f"Content length: {len(content)}")
    if "cloudflare" in content.lower():
        print("Failed: cloudflare challenge detected")
    else:
        print("Succeeded! First 200 chars:")
        print(content[:200])

if __name__ == "__main__":
    asyncio.run(main())
