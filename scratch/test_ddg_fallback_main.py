import asyncio
import sys
import os

# Set up python path to import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import fallback_search_genetics

async def test():
    print("Testing fallback_search_genetics('Qrazy Train')...")
    parents = await fallback_search_genetics("Qrazy Train")
    print(f"Result: {parents}")

if __name__ == "__main__":
    asyncio.run(test())
