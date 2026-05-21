import asyncio
import logging
import sys

# Add src to python path
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.collectors.seedfinder_collector import search_seedfinder

logging.basicConfig(level=logging.INFO)

async def main():
    for query in ["Jacks Cleaner", "Jacks Cleaner 2", "Jacks Cleaner Bx"]:
        print(f"--- Searching for: {query} ---")
        results = await search_seedfinder(query)
        for r in results:
            print(f"Name: {r['name']}, Breeder: {r['breeder']}, Strain Slug: {r['strain_slug']}, Breeder Slug: {r['breeder_slug']}")

if __name__ == "__main__":
    asyncio.run(main())
