import asyncio
import httpx
import re

async def main():
    headers = {"User-Agent": "CannabisResearcher/1.0 (academic research)"}
    urls = [
        "https://kannapedia.net/strains",
        "https://www.kannapedia.net/strains",
    ]
    for url in urls:
        print(f"--- Fetching {url} ---")
        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True, headers=headers) as client:
                resp = await client.get(url)
                print(f"Status Code: {resp.status_code}")
                print(f"Final URL: {resp.url}")
                print(f"Content Length: {len(resp.text)}")
                
                # Check for blocking
                if "block" in resp.text.lower() or "cloudflare" in resp.text.lower() or "captcha" in resp.text.lower():
                    print("Potential block/captcha page detected!")
                    print(resp.text[:1000])
                    continue
                
                # Find matching patterns
                pattern = r'data-name="([^"]+)"[^>]*>\s*<a\s+href="/strains/(rsp\d+)"'
                matches = re.findall(pattern, resp.text, re.IGNORECASE)
                print(f"Found {len(matches)} matches using regex.")
                if matches:
                    print("Sample matches:")
                    for m in matches[:10]:
                        print(m)
                else:
                    # Let's search for "qrazy" or "train" or any "rsp" links in the HTML
                    rsp_links = re.findall(r'/strains/rsp\d+', resp.text, re.IGNORECASE)
                    print(f"Found {len(rsp_links)} raw '/strains/rsp...' links.")
                    if rsp_links:
                        print("Sample links:", rsp_links[:10])
                    # Print a snippet of the body to see what the page looks like
                    print("HTML snippet around body:")
                    body_start = resp.text.find("<body")
                    if body_start != -1:
                        print(resp.text[body_start:body_start+2000])
                    else:
                        print(resp.text[:2000])
                        
        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
