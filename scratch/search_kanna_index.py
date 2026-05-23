import asyncio
import httpx
import re

async def main():
    headers = {"User-Agent": "CannabisResearcher/1.0 (academic research)"}
    url = "https://kannapedia.net/strains"
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True, headers=headers) as client:
            resp = await client.get(url)
            html = resp.text
            
            # Print total matches containing 'qrazy' or 'train'
            for term in ["qrazy", "train"]:
                matches = re.findall(rf'data-name="([^"]*{term}[^"]*)"[^>]*>\s*<a\s+href="/strains/(rsp\d+)"', html, re.IGNORECASE)
                print(f"Matches containing '{term}':")
                for m in matches:
                    print(m)
                    
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
