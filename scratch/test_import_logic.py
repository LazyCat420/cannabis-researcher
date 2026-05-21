import asyncio
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set environment variable
os.environ["SCRAPER_SERVICE_URL"] = "http://10.0.0.16:8001"

from main import _is_post_relevant
from src.scraper_client import ScraperClient

logging.basicConfig(level=logging.INFO)

async def test_import_for(strain_name):
    print(f"\n==================================================")
    print(f"TESTING IMPORT FOR: {strain_name}")
    print(f"==================================================")
    
    scraper_client = ScraperClient()
    try:
        search_query = strain_name
        # Overgrow
        print("\n--- Scrape Overgrow ---")
        try:
            search_res = await scraper_client.collect({
                "source": "discourse",
                "base_url": "https://overgrow.com",
                "forum_name": "overgrow",
                "query": f'"{search_query}"',
                "limit": 10
            })
            topic_ids = []
            for item in search_res.get("items", []):
                tid = item.get("topic_id")
                if tid and tid not in topic_ids:
                    topic_ids.append(tid)
                if len(topic_ids) >= 3:
                    break
            print(f"Found {len(topic_ids)} unique Overgrow topic IDs: {topic_ids}")
            
            for tid in topic_ids:
                print(f"Fetching posts for topic ID: {tid}")
                posts_og = await scraper_client.collect({
                    "source": "discourse",
                    "base_url": "https://overgrow.com",
                    "forum_name": "overgrow",
                    "topic_id": tid,
                    "limit": 30
                })
                posts = posts_og.get("items", [])
                print(f"  Fetched {len(posts)} posts. Checking relevance...")
                relevant_count = 0
                image_count = 0
                for p in posts:
                    title = p.get("title", "")
                    body = p.get("body", "")
                    relevant = _is_post_relevant(body, title, search_query)
                    if relevant:
                        relevant_count += 1
                        image_urls = p.get("image_urls", [])
                        image_count += len(image_urls)
                        if image_urls:
                            print(f"    [RELEVANT] Post {p.get('id')} by {p.get('author')} has images: {image_urls}")
                print(f"  Relevance check: {relevant_count} / {len(posts)} posts are relevant, containing {image_count} images.")
        except Exception as ex:
            print(f"Failed Overgrow: {ex}")

        # Rollitup
        print("\n--- Scrape Rollitup ---")
        def normalize_xenforo_thread_url(url: str) -> str:
            if not url:
                return ""
            if "/post-" in url:
                url = url.split("/post-")[0]
            if not url.endswith("/"):
                url += "/"
            return url

        try:
            search_res = await scraper_client.collect({
                "source": "xenforo",
                "base_url": "https://www.rollitup.org",
                "forum_name": "rollitup",
                "query": f'"{search_query}"',
                "limit": 10
            })
            thread_urls = []
            for item in search_res.get("items", []):
                turl = normalize_xenforo_thread_url(item.get("url"))
                if turl and turl not in thread_urls:
                    thread_urls.append(turl)
                if len(thread_urls) >= 3:
                    break
            print(f"Found {len(thread_urls)} unique Rollitup thread URLs: {thread_urls}")
            
            for turl in thread_urls:
                print(f"Fetching posts for thread URL: {turl}")
                posts_riu = await scraper_client.collect({
                    "source": "xenforo",
                    "base_url": "https://www.rollitup.org",
                    "forum_name": "rollitup",
                    "thread_url": turl,
                    "limit": 30
                })
                posts = posts_riu.get("items", [])
                print(f"  Fetched {len(posts)} posts. Checking relevance...")
                relevant_count = 0
                image_count = 0
                for p in posts:
                    title = p.get("title", "")
                    body = p.get("body", "")
                    relevant = _is_post_relevant(body, title, search_query)
                    if relevant:
                        relevant_count += 1
                        image_urls = p.get("image_urls", [])
                        image_count += len(image_urls)
                        if image_urls:
                            print(f"    [RELEVANT] Post {p.get('id')} by {p.get('author')} has images: {image_urls}")
                print(f"  Relevance check: {relevant_count} / {len(posts)} posts are relevant, containing {image_count} images.")
        except Exception as ex:
            print(f"Failed Rollitup: {ex}")

    finally:
        await scraper_client.close()

async def main():
    for strain in ["Jacks Cleaner", "Jacks Cleaner 2", "Jacks Cleaner Bx"]:
        await test_import_for(strain)

if __name__ == "__main__":
    asyncio.run(main())
