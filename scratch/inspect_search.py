import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["SCRAPER_SERVICE_URL"] = "http://10.0.0.16:8001"

from src.scraper_client import ScraperClient

async def main():
    client = ScraperClient()
    try:
        res = await client.collect({
            "source": "xenforo",
            "base_url": "https://www.rollitup.org",
            "forum_name": "rollitup",
            "query": '"Jacks Cleaner 2"',
            "limit": 5
        })
        print("Xenforo search results:")
        for item in res.get("items", []):
            print(f"ID: {item.get('id')}")
            print(f"URL: {item.get('url')}")
            print(f"Title: {item.get('title')}")
            print(f"Body: {item.get('body')[:100]}...")
            print("-" * 40)
            
        res_og = await client.collect({
            "source": "discourse",
            "base_url": "https://overgrow.com",
            "forum_name": "overgrow",
            "query": '"Jacks Cleaner 2"',
            "limit": 5
        })
        print("\nDiscourse search results:")
        for item in res_og.get("items", []):
            print(f"ID: {item.get('id')}")
            print(f"Topic ID: {item.get('topic_id')}")
            print(f"URL: {item.get('url')}")
            print(f"Title: {item.get('title')}")
            print(f"Body: {item.get('body')[:100]}...")
            print("-" * 40)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
