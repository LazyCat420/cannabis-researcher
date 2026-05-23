import asyncio
import httpx
import json

async def main():
    url = "https://www.reddit.com/r/microgrowery/search.json"
    params = {
        "q": "soil",
        "restrict_sr": "on",
        "limit": 10,
    }
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    async with httpx.AsyncClient(timeout=15, follow_redirects=True, headers=headers) as client:
        r = await client.get(url, params=params)
        print(f"Status Code: {r.status_code}")
        print(f"Response URL: {r.url}")
        print(f"Response Headers: {dict(r.headers)}")
        try:
            data = r.json()
            posts = data.get("data", {}).get("children", [])
            print(f"Found {len(posts)} total posts on Reddit.")
            for i, p_wrapper in enumerate(posts):
                p = p_wrapper.get("data", {})
                print(f"\n--- Post {i+1} ---")
                print(f"Title: {p.get('title')}")
                print(f"Score: {p.get('score')}")
                print(f"Comments: {p.get('num_comments')}")
                print(f"Over 18 (NSFW): {p.get('over_18')}")
                print(f"Selftext length: {len(p.get('selftext', ''))}")
                
                # Check quality filters
                reasons = []
                if p.get("selftext") in ("[removed]", "[deleted]"):
                    reasons.append("removed/deleted")
                if p.get("over_18"):
                    reasons.append("over_18 (NSFW)")
                if p.get("score", 0) < 3:
                    reasons.append(f"score < 3 ({p.get('score')})")
                if p.get("num_comments", 0) < 2:
                    reasons.append(f"comments < 2 ({p.get('num_comments')})")
                if len(p.get("selftext", "")) < 50 and p.get("score", 0) < 50:
                    reasons.append("short body & score < 50")
                    
                if reasons:
                    print(f"FAIL QUALITY FILTER: {', '.join(reasons)}")
                else:
                    print("PASS QUALITY FILTER")
        except Exception as e:
            print(f"JSON Parse failed: {e}")
            print(f"Raw Text (first 500 chars): {r.text[:500]}")

if __name__ == "__main__":
    asyncio.run(main())
