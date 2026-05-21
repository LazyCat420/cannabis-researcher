import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["SCRAPER_SERVICE_URL"] = "http://10.0.0.16:8001"

from src.scraper_client import ScraperClient

async def main():
    client = ScraperClient()
    try:
        # Let's request the direct search result URL for XenForo
        post_url = "https://www.rollitup.org/t/name-me-a-strain-better-than-vortex.1082808/post-17173530"
        print(f"Fetching XenForo posts for: {post_url}")
        res = await client.collect({
            "source": "xenforo",
            "base_url": "https://www.rollitup.org",
            "forum_name": "rollitup",
            "thread_url": post_url,
            "limit": 30
        })
        
        posts = res.get("items", [])
        print(f"Fetched {len(posts)} posts.")
        found_post = False
        for p in posts:
            if "17173530" in p.get("id", "") or "17173530" in p.get("url", ""):
                print(f"Found post 17173530 by {p.get('author')}:")
                print(f"Body snippet: {p.get('body')[:200]}")
                found_post = True
                break
        if not found_post and posts:
            print("Post not found. First post in fetched list:")
            print(f"ID: {posts[0].get('id')} by {posts[0].get('author')}")
            print(f"Body: {posts[0].get('body')[:200]}")

        # Let's request Discourse post URL
        disc_url = "https://overgrow.com/t/tga-subcool-gear/30518/392"
        # Wait, how does Discourse collection handle topic ID?
        # In main.py, it uses topic_id.
        # But wait! If we pass topic_id, how does the scraper service fetch it?
        # Discourse collector has category/topic/search.
        # If we query a specific post in a Discourse thread, we can fetch posts around it.
        # Let's check how the discourse collector gets posts.
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
