import asyncio
import json
import os
import sys
import re

def parse_genetics_from_snippets(snippets, strain_name):
    name_norm = re.sub(r'[^a-zA-Z0-9]', '', strain_name.lower())
    for snip in snippets:
        snip_clean = snip.replace('\xa0', ' ').replace('\u200e', '')
        
        # Strategy 1: Look for "StrainName »»» Parent1 x Parent2" or similar
        match = re.search(r'»»»\s*([^·\n]+)', snip_clean)
        if match:
            cross_text = match.group(1).strip()
            if any(x in cross_text.lower() for x in [' x ', '×', ' x']):
                parts = re.split(r'\s+[xX×]\s+|\s+x\s+|_x_|_X_', cross_text)
                parents = [p.strip() for p in parts if p.strip()]
                parents = [p for p in parents if len(p) > 2 and p.lower() not in ["mostly indica", "mostly sativa", "hybrid"]]
                if len(parents) >= 2:
                    return parents
                    
        # Strategy 2: Look for "Genetic:Parent1 x Parent2"
        match_genetic = re.search(r'Genetic\s*:\s*([^.\n]+)', snip_clean, re.IGNORECASE)
        if match_genetic:
            cross_text = match_genetic.group(1).strip()
            cross_text = re.split(r'flowering|characteristics|strong|medicinal', cross_text, flags=re.IGNORECASE)[0].strip()
            if any(x in cross_text.lower() for x in [' x ', '×', ' x']):
                parts = re.split(r'\s+[xX×]\s+|\s+x\s+|_x_|_X_', cross_text)
                parents = [p.strip() for p in parts if p.strip()]
                parents = [p for p in parents if len(p) > 2 and p.lower() not in ["mostly indica", "mostly sativa", "hybrid"]]
                if len(parents) >= 2:
                    return parents
                    
        # Strategy 3: Heuristic for Capitalized Words separated by 'x'
        for match in re.finditer(r'([A-Z][a-zA-Z0-9\s\']+)\s+[xX×*]\s+([A-Z][a-zA-Z0-9\s\']+)(?:\s+[xX×*]\s+([A-Z][a-zA-Z0-9\s\']+))?', snip_clean):
            parents = [p.strip() for p in match.groups() if p]
            parents = [p for p in parents if len(p) > 2 and p.lower() not in ["mostly indica", "mostly sativa", "hybrid"] and len(p) < 40]
            if len(parents) >= 2:
                return parents
    return []

async def test_ddg_subprocess():
    python_exe = "/home/lazycat/github/rods-project/sun/scraper-service/.venv/bin/python"
    if not os.path.exists(python_exe):
        python_exe = "/home/lazycat/github/rods-project/sun/scraper-service/venv/bin/python"
        
    query = 'site:seedfinder.eu "Qrazy Train"'
    script = """
import sys
import json
try:
    from ddgs import DDGS
    with DDGS() as ddgs:
        results = list(ddgs.text(sys.argv[1], max_results=10))
    print(json.dumps({"success": True, "results": results}))
except Exception as e:
    print(json.dumps({"success": False, "error": str(e)}))
"""
    print(f"Running search via {python_exe} for: {query}")
    proc = await asyncio.create_subprocess_exec(
        python_exe, "-c", script, query,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode == 0:
        data = json.loads(stdout.decode().strip())
        if data.get("success"):
            results = data.get("results", [])
            print(f"Found {len(results)} search results.")
            snippets = [r.get("body", "") for r in results if r.get("body")]
            for idx, snip in enumerate(snippets):
                print(f"Snippet {idx+1}: {snip}")
            parents = parse_genetics_from_snippets(snippets, "Qrazy Train")
            print(f"Parsed parents: {parents}")
        else:
            print(f"Execution error: {data.get('error')}")
    else:
        print(f"Process failed with code {proc.returncode}: {stderr.decode()}")

if __name__ == "__main__":
    asyncio.run(test_ddg_subprocess())
