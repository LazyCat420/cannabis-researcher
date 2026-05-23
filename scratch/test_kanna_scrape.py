import os
os.environ["SCRAPER_SERVICE_URL"] = "http://10.0.0.16:8001"

import asyncio
import json
from src.scraper_client import ScraperClient

async def run():
    client = ScraperClient()
    try:
        print("Calling collect_kannapedia for 'Headband'...")
        results = await client.collect_kannapedia("Headband", limit=3)
        print(f"Scraped {len(results)} items.")
        for i, item in enumerate(results):
            print(f"\n--- Item {i+1} ---")
            print("Name:", item.get("name"))
            print("RSP Number:", item.get("rsp_number"))
            print("Source URL:", item.get("source_url"))
            print("General Info Keys:", list(item.get("general_info", {}).keys()))
            print("General Info:", json.dumps(item.get("general_info"), indent=2))
            print("Keys:", list(item.keys()))
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(run())
