import asyncio
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.scraper_client import ScraperClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    client = ScraperClient(base_url="http://10.0.0.16:8001")
    
    # Let's fetch the posts of the THCFarmer thread we found: https://www.thcfarmer.com/threads/jack-herer.174402/
    logger.info("--- Testing direct thread fetch on THCFarmer ---")
    posts = await client.collect({
        "source": "xenforo",
        "base_url": "https://www.thcfarmer.com",
        "forum_name": "thcfarmer",
        "thread_url": "https://www.thcfarmer.com/threads/jack-herer.174402/",
        "limit": 10
    })
    logger.info(f"Thread posts count: {posts.get('count', 0)}")
    if 'error' in posts:
        logger.error(f"Error: {posts['error']}")
    for item in posts.get("items", []):
        logger.info(f"Post #{item.get('post_number')} by {item.get('author')}")
        logger.info(f"Body snippet: {item.get('body')[:150]}")
        logger.info(f"Image URLs: {item.get('image_urls')}")

    # Let's fetch the posts of the Overgrow topic we found: topic_id = 145074
    logger.info("--- Testing direct topic fetch on Overgrow ---")
    posts = await client.collect({
        "source": "discourse",
        "base_url": "https://overgrow.com",
        "forum_name": "overgrow",
        "topic_id": 145074,
        "limit": 10
    })
    logger.info(f"Topic posts count: {posts.get('count', 0)}")
    for item in posts.get("items", []):
        logger.info(f"Post #{item.get('post_number')} by {item.get('author')}")
        logger.info(f"Body snippet: {item.get('body')[:150]}")
        logger.info(f"Image URLs: {item.get('image_urls')}")

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
