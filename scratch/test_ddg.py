import httpx
from bs4 import BeautifulSoup
import asyncio

async def test_lite():
    query = '"Headband" (site:overgrow.com OR site:rollitup.org OR site:thcfarmer.com OR site:icmag.com)'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        # For /lite/ we POST the query as q
        r = await client.post("https://lite.duckduckgo.com/lite/", data={"q": query}, headers=headers)
        print("Status Code:", r.status_code)
        if r.status_code != 200:
            print("Response:", r.text[:200])
            return
        
        soup = BeautifulSoup(r.text, "html.parser")
        links = []
        for a in soup.select("a.result-link"):
            href = a.get("href")
            if href:
                links.append(href)
        
        print(f"Found {len(links)} links:")
        for l in links[:15]:
            print(" -", l)

if __name__ == "__main__":
    asyncio.run(test_lite())
