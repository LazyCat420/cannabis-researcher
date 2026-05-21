import asyncio
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set environment variable
os.environ["SCRAPER_SERVICE_URL"] = "http://10.0.0.16:8001"

from src.scraper_client import ScraperClient

logging.basicConfig(level=logging.INFO)

async def test_for_strain(strain):
    print(f"\n==================== Testing: {strain} ====================")
    client = ScraperClient()
    
    # Try discourse (Overgrow) search
    print("--- Searching Overgrow ---")
    try:
        search_res = await client.collect({
            "source": "discourse",
            "base_url": "https://overgrow.com",
            "forum_name": "overgrow",
            "query": f'"{strain}"',
            "limit": 5
        })
        items = search_res.get("items", [])
        print(f"Overgrow search returned {len(items)} items.")
        for item in items[:3]:
            print(f"  Topic ID: {item.get('topic_id')}, Title: {item.get('title')}, URL: {item.get('url')}")
            print(f"  Images ({len(item.get('image_urls', []))}): {item.get('image_urls')}")
    except Exception as e:
        print(f"Overgrow failed: {e}")

    # Try xenforo (Rollitup) search
    print("--- Searching Rollitup ---")
    try:
        search_res = await client.collect({
            "source": "xenforo",
            "base_url": "https://www.rollitup.org",
            "forum_name": "rollitup",
            "query": f'"{strain}"',
            "limit": 5
        })
        items = search_res.get("items", [])
        print(f"Rollitup search returned {len(items)} items.")
        for item in items[:3]:
            print(f"  ID: {item.get('id')}, Title: {item.get('title')}, URL: {item.get('url')}")
            print(f"  Images ({len(item.get('image_urls', []))}): {item.get('image_urls')}")
    except Exception as e:
        print(f"Rollitup failed: {e}")

    await client.close()

async def main():
    for strain in ["Jacks Cleaner", "Jacks Cleaner 2", "Jacks Cleaner Bx"]:
        await test_for_strain(strain)

if __name__ == "__main__":
    asyncio.run(main())
