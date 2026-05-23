import asyncio
import httpx
import logging
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("audit_scrapers")

BASE_URL = "http://localhost:8001"

async def test_endpoint(name: str, payload: dict):
    logger.info(f"\n========================================\nTesting Endpoint: {name}\n========================================")
    url = f"{BASE_URL}/collect"
    async with httpx.AsyncClient(timeout=40.0) as client:
        try:
            logger.info(f"Payload: {json.dumps(payload, indent=2)}")
            r = await client.post(url, json=payload)
            logger.info(f"Status Code: {r.status_code}")
            if r.status_code != 200:
                logger.error(f"Response: {r.text}")
                return False
            
            data = r.json()
            if data.get("error"):
                logger.error(f"Endpoint returned error: {data['error']}")
            
            count = data.get("count", 0)
            items = data.get("items", [])
            logger.info(f"SUCCESS! Retrieved {count} items.")
            
            # Print first item snippet if available
            if items:
                logger.info(f"Sample Item (1 of {count}):")
                first = items[0]
                logger.info(f"  ID: {first.get('id')}")
                logger.info(f"  Title: {first.get('title') or first.get('name')}")
                logger.info(f"  URL: {first.get('url')}")
                body = first.get('body') or first.get('description') or ""
                logger.info(f"  Body (150 char limit): {body[:150]}...")
                logger.info(f"  Images count: {len(first.get('image_urls', []))}")
            else:
                logger.warning("No items returned.")
            return True
        except Exception as e:
            logger.exception(f"Exception during test of {name}: {e}")
            return False

async def main():
    # 1. Test Discourse Search (Overgrow)
    await test_endpoint("Discourse Search (Overgrow)", {
        "source": "discourse",
        "base_url": "https://overgrow.com",
        "forum_name": "overgrow",
        "query": "Jacks Cleaner",
        "limit": 3
    })

    # 2. Test Discourse Tag (Overgrow)
    await test_endpoint("Discourse Tag (Overgrow)", {
        "source": "discourse",
        "base_url": "https://overgrow.com",
        "forum_name": "overgrow",
        "tag": "breeding",
        "limit": 3
    })

    # 3. Test XenForo Search (Rollitup)
    await test_endpoint("XenForo Search (Rollitup)", {
        "source": "xenforo",
        "base_url": "https://www.rollitup.org",
        "forum_name": "rollitup",
        "query": "Jacks Cleaner",
        "limit": 3
    })

    # 4. Test XenForo Subforum (Rollitup)
    await test_endpoint("XenForo Subforum (Rollitup)", {
        "source": "xenforo",
        "base_url": "https://www.rollitup.org",
        "forum_name": "rollitup",
        "subforum_path": "f/grow-journals.54/",
        "limit": 3
    })

    # 5. Test Kannapedia Search
    await test_endpoint("Kannapedia Search", {
        "source": "kannapedia",
        "query": "Jack Herer",
        "limit": 3
    })

    # 6. Test Reddit Search
    await test_endpoint("Reddit Search", {
        "source": "reddit",
        "subreddits": ["microgrowery"],
        "query": "Jacks Cleaner",
        "limit": 3
    })

if __name__ == "__main__":
    asyncio.run(main())
