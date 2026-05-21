import asyncio
import logging
import sys
import os

# Add parent directory to sys.path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.collectors.seedfinder_collector import search_seedfinder, scrape_seedfinder_strain
from src.scraper_client import ScraperClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

async def main():
    logger.info("=== Starting Jack Herer Scrape Test ===")
    
    # 1. Test SeedFinder
    logger.info("--- 1. Testing SeedFinder ---")
    try:
        results = await search_seedfinder("Jack Herer", limit=5)
        logger.info(f"SeedFinder search results count: {len(results)}")
        for r in results:
            logger.info(f"Found strain: {r['name']} by {r['breeder']} (URL: {r['url']})")
            # Try to scrape the detail for the first match
            if r == results[0]:
                detail = await scrape_seedfinder_strain(r['strain_slug'], r['breeder_slug'])
                if detail:
                    logger.info(f"Detail name: {detail['name']}")
                    logger.info(f"Type: {detail['type']}")
                    logger.info(f"Flowering days: {detail['flowering_time_days']}")
                    logger.info(f"Lineage count: {len(detail['lineage'])}")
                    logger.info(f"Awards count: {len(detail['awards'])}")
                    logger.info(f"Description length: {len(detail['description']) if detail['description'] else 0}")
                else:
                    logger.warning("Failed to fetch detail for first strain.")
    except Exception as e:
        logger.error(f"SeedFinder test failed: {e}")

    # 2. Test Overgrow (Discourse) Search
    logger.info("--- 2. Testing Overgrow (Discourse) Search ---")
    client = ScraperClient(base_url="http://10.0.0.16:8001") # Scraper service runs on NAS IP
    try:
        posts = await client.collect({
            "source": "discourse",
            "base_url": "https://overgrow.com",
            "forum_name": "overgrow",
            "query": "Jack Herer",
            "limit": 10
        })
        logger.info(f"Overgrow search count: {posts.get('count', 0)}")
        if 'error' in posts:
            logger.error(f"Overgrow error: {posts['error']}")
        for item in posts.get("items", [])[:3]:
            logger.info(f"Post title: {item.get('title')} by {item.get('author')}")
            logger.info(f"URL: {item.get('url')}")
            logger.info(f"Image URLs: {item.get('image_urls')}")
    except Exception as e:
        logger.error(f"Overgrow search test failed: {e}")

    # 3. Test Rollitup (XenForo) Search
    logger.info("--- 3. Testing Rollitup (XenForo) Search ---")
    try:
        posts = await client.collect({
            "source": "xenforo",
            "base_url": "https://www.rollitup.org",
            "forum_name": "rollitup",
            "query": "Jack Herer",
            "limit": 10
        })
        logger.info(f"Rollitup search count: {posts.get('count', 0)}")
        if 'error' in posts:
            logger.error(f"Rollitup error: {posts['error']}")
        for item in posts.get("items", [])[:3]:
            logger.info(f"Post title: {item.get('title')} by {item.get('author')}")
            logger.info(f"URL: {item.get('url')}")
            logger.info(f"Image URLs: {item.get('image_urls')}")
    except Exception as e:
        logger.error(f"Rollitup search test failed: {e}")

    # 4. Test THCFarmer (XenForo) Search
    logger.info("--- 4. Testing THCFarmer (XenForo) Search ---")
    try:
        posts = await client.collect({
            "source": "xenforo",
            "base_url": "https://www.thcfarmer.com",
            "forum_name": "thcfarmer",
            "query": "Jack Herer",
            "limit": 10
        })
        logger.info(f"THCFarmer search count: {posts.get('count', 0)}")
        if 'error' in posts:
            logger.error(f"THCFarmer error: {posts['error']}")
        for item in posts.get("items", [])[:3]:
            logger.info(f"Post title: {item.get('title')} by {item.get('author')}")
            logger.info(f"URL: {item.get('url')}")
            logger.info(f"Image URLs: {item.get('image_urls')}")
    except Exception as e:
        logger.error(f"THCFarmer search test failed: {e}")

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
