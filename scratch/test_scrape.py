import asyncio
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.collectors.seedfinder_collector import scrape_seedfinder_strain

logging.basicConfig(level=logging.INFO)

async def main():
    strain_slug = "qrazy-train"
    breeder_slug = "subcools-the-dank"
    print(f"--- Scraping strain: {strain_slug} / {breeder_slug} ---")
    data = await scrape_seedfinder_strain(strain_slug, breeder_slug)
    if data:
        print("Scraped successfully! Data:")
        for k, v in data.items():
            if k in ["description", "lineage", "hybrids"]:
                print(f"{k}: {len(v) if v else None} items/chars")
            else:
                print(f"{k}: {v}")
    else:
        print("Failed to scrape strain data (returned None)")

if __name__ == "__main__":
    asyncio.run(main())
