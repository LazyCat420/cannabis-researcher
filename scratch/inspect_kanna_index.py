import asyncio
import re
import httpx

async def run():
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        resp = await client.get("https://kannapedia.net/strains")
        resp.raise_for_status()
        html = resp.text

    print(f"Total HTML length: {len(html)}")
    
    # Print a few examples of raw data-name match lines
    matches = list(re.finditer(r'data-name="([^"]+)"[^>]*>\s*<a\s+href="/strains/(rsp\d+)"', html, re.IGNORECASE))
    print(f"Total matching elements in regex: {len(matches)}")
    
    print("\nStrains containing 'head' (case-insensitive):")
    count = 0
    for m in matches:
        name = m.group(1).strip()
        rsp = m.group(2).strip()
        if "head" in name.lower():
            print(f"- Name: {repr(name)}, RSP: {repr(rsp)}")
            count += 1
    print(f"Found {count} strains containing 'head'.")

if __name__ == "__main__":
    asyncio.run(run())
