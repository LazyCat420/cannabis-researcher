import asyncio
import re
import httpx
from ddgs import DDGS

async def main():
    query = "Jacks Cleaner"
    subreddit = "microgrowery"
    ddg_query = f"site:reddit.com/r/{subreddit} {query}"
    print(f"Querying DDG: {ddg_query}")
    
    try:
        with DDGS() as ddgs:
            ddg_results = list(ddgs.text(ddg_query, max_results=5))
            
        print(f"Found {len(ddg_results)} results on DDG.")
        for item in ddg_results:
            href = item.get("href", "")
            title = item.get("title", "")
            print(f"- {title}: {href}")
            
            # Extract reddit comment link
            # Format: https://www.reddit.com/r/microgrowery/comments/xxxxxx/title_slug/
            match = re.search(r"(reddit\.com/r/[^/]+/comments/[a-z0-9]+)", href, re.IGNORECASE)
            if match:
                json_url = "https://" + match.group(1) + ".json"
                print(f"  Fetching JSON: {json_url}")
                
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                async with httpx.AsyncClient(timeout=15, follow_redirects=True, headers=headers) as client:
                    r = await client.get(json_url)
                    print(f"  Status Code: {r.status_code}")
                    if r.status_code == 200:
                        data = r.json()
                        # Reddit thread JSON is a list of two items: [post_data, comments_data]
                        post_info = data[0].get("data", {}).get("children", [{}])[0].get("data", {})
                        print(f"  Post Title: {post_info.get('title')}")
                        print(f"  Post Score: {post_info.get('score')}")
                        print(f"  Post Comments: {post_info.get('num_comments')}")
                        print(f"  Selftext Length: {len(post_info.get('selftext', ''))}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
