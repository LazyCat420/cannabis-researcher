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
    logger.info("=== Starting Jacks Cleaner Scrape Test ===")
    
    # 1. Test SeedFinder
    logger.info("\n--- 1. Testing SeedFinder ---")
    try:
        results = await search_seedfinder("Jacks Cleaner", limit=5)
        logger.info(f"SeedFinder search results count: {len(results)}")
        for r in results:
            logger.info(f"Found strain: {r['name']} by {r['breeder']} (URL: {r['url']})")
            # Try to scrape the detail for the match
            detail = await scrape_seedfinder_strain(r['strain_slug'], r['breeder_slug'])
            if detail:
                logger.info(f"Detail name: {detail.get('name')}")
                logger.info(f"Breeder: {detail.get('breeder')}")
                logger.info(f"Type: {detail.get('type')}")
                logger.info(f"Flowering days: {detail.get('flowering_time_days')}")
                logger.info(f"Lineage: {detail.get('lineage')}")
                logger.info(f"Awards: {detail.get('awards')}")
                logger.info(f"Description length: {len(detail.get('description')) if detail.get('description') else 0}")
            else:
                logger.warning(f"Failed to fetch detail for strain: {r['name']}")
    except Exception as e:
        logger.error(f"SeedFinder test failed: {e}")

    # Initialize ScraperClient.
    client = ScraperClient(base_url="http://10.0.0.16:8001")
    
    # Let's check health of scraper-service first (without closing the client)
    logger.info("\n--- Checking Scraper Service Health ---")
    try:
        resp = await client.client.get(f"{client.base_url}/health")
        logger.info(f"Scraper service health: status={resp.status_code}, body={resp.text}")
    except Exception as e:
        logger.warning(f"Failed to reach scraper-service on {client.base_url}: {e}")
        # Try localhost:8001
        client = ScraperClient(base_url="http://localhost:8001")
        try:
            resp = await client.client.get(f"{client.base_url}/health")
            logger.info(f"Fallback localhost scraper service health: status={resp.status_code}, body={resp.text}")
        except Exception as ex:
            logger.error(f"Failed to reach scraper-service on localhost: {ex}")

    # 2. Test Overgrow (Discourse) Search
    logger.info("\n--- 2. Testing Overgrow (Discourse) Search for 'Jacks Cleaner' ---")
    try:
        posts = await client.collect({
            "source": "discourse",
            "base_url": "https://overgrow.com",
            "forum_name": "overgrow",
            "query": "Jacks Cleaner",
            "limit": 10
        })
        logger.info(f"Overgrow search count: {posts.get('count', 0)}")
        if 'error' in posts:
            logger.error(f"Overgrow error: {posts['error']}")
        for item in posts.get("items", []):
            logger.info(f"Post title: {item.get('title')} by {item.get('author')}")
            logger.info(f"URL: {item.get('url')}")
            logger.info(f"Image URLs: {item.get('image_urls')}")
            logger.info(f"Body snippet: {item.get('body')[:150]}...")
    except Exception as e:
        logger.error(f"Overgrow search test failed: {e}")

    # 3. Test Rollitup (XenForo) Search
    logger.info("\n--- 3. Testing Rollitup (XenForo) Search for 'Jacks Cleaner' ---")
    try:
        posts = await client.collect({
            "source": "xenforo",
            "base_url": "https://www.rollitup.org",
            "forum_name": "rollitup",
            "query": "Jacks Cleaner",
            "limit": 10
        })
        logger.info(f"Rollitup search count: {posts.get('count', 0)}")
        if 'error' in posts:
            logger.error(f"Rollitup error: {posts['error']}")
        for item in posts.get("items", []):
            logger.info(f"Post title: {item.get('title')} by {item.get('author')}")
            logger.info(f"URL: {item.get('url')}")
            logger.info(f"Image URLs: {item.get('image_urls')}")
            logger.info(f"Body snippet: {item.get('body')[:150]}...")
    except Exception as e:
        logger.error(f"Rollitup search test failed: {e}")

    # 4. Test THCFarmer (XenForo) Search
    logger.info("\n--- 4. Testing THCFarmer (XenForo) Search for 'Jacks Cleaner' ---")
    try:
        posts = await client.collect({
            "source": "xenforo",
            "base_url": "https://www.thcfarmer.com",
            "forum_name": "thcfarmer",
            "query": "Jacks Cleaner",
            "limit": 10
        })
        logger.info(f"THCFarmer search count: {posts.get('count', 0)}")
        if 'error' in posts:
            logger.error(f"THCFarmer error: {posts['error']}")
        for item in posts.get("items", []):
            logger.info(f"Post title: {item.get('title')} by {item.get('author')}")
            logger.info(f"URL: {item.get('url')}")
            logger.info(f"Image URLs: {item.get('image_urls')}")
            logger.info(f"Body snippet: {item.get('body')[:150]}...")
    except Exception as e:
        logger.error(f"THCFarmer search test failed: {e}")

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
