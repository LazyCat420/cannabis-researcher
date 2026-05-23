import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.scraper_client import ScraperClient

async def main():
    s = ScraperClient()
    res = await s.scrape("https://seedfinder.eu/en/database/strains/alphabetical/Q", engine="playwright", options={"raw_html": True})
    content = res.get("content", "") or ""
    print(f"Content length: {len(content)}")
    if len(content) < 500:
        print(f"Content: {content}")
    # Find any links containing "/strain-info/"
    import re
    links = re.findall(r'href="[^"]*strain-info[^"]*"', content)
    print(f"Found {len(links)} links with strain-info")
    for l in links[:10]:
        print(l)
        
    # Also find all a tags to see what's in there
    a_tags = re.findall(r'<a[^>]*href=[^>]*>.*?</a>', content, re.IGNORECASE)[:20]
    print(f"\nFirst 20 standard a tags:")
    for tag in a_tags:
        print(tag)
        
    await s.close()

if __name__ == "__main__":
    asyncio.run(main())
