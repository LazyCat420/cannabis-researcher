import asyncio
import httpx
import re

async def main():
    headers = {"User-Agent": "CannabisResearcher/1.0 (academic research)"}
    url = "https://kannapedia.net/strains"
    
    async with httpx.AsyncClient(timeout=15, follow_redirects=True, headers=headers) as client:
        resp = await client.get(url)
        html = resp.text

    import difflib

    query = "Jacks Cleaner"
    query_lower = query.strip().lower()
    q_norm = re.sub(r'[^a-z0-9]', '', query_lower)
    candidates = []

    print(f"--- Searching for candidates matching '{query}' ---")
    pattern = r'data-name="([^"]+)"[^>]*>\s*<a\s+href="/strains/(rsp\d+)"'
    for m in re.finditer(pattern, html, re.IGNORECASE):
        strain_name = m.group(1).strip()
        rsp = m.group(2).strip()
        s_norm = re.sub(r'[^a-z0-9]', '', strain_name.lower())
        
        # Calculate ratio
        ratio = difflib.SequenceMatcher(None, q_norm, s_norm).ratio()
        
        # Exact match = 100, substring matches have high score, fuzzy matches have score based on ratio
        score = 0
        if q_norm == s_norm:
            score = 100
        elif s_norm.startswith(q_norm) or q_norm.startswith(s_norm):
            score = 90
        elif q_norm in s_norm or s_norm in q_norm:
            score = 80
        elif ratio >= 0.8:
            score = int(ratio * 100)
            
        if score > 0:
            candidates.append((score, strain_name, rsp))
            
    print(f"Candidates found: {len(candidates)}")
    for score, strain_name, rsp in sorted(candidates, key=lambda x: x[0], reverse=True)[:10]:
        print(f"Score: {score} | Name: {strain_name} | RSP: {rsp}")



if __name__ == "__main__":
    asyncio.run(main())
