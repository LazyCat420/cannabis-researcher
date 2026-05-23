import asyncio
import httpx
import json

SCRAPER_URL = "http://10.0.0.16:8001"

async def test_source(payload):
    source = payload.get("source")
    target = payload.get("query") or payload.get("thread_url") or payload.get("rsp_numbers")
    print(f"\n--- Testing source: {source} for {target} ---")
    try:
        async with httpx.AsyncClient(timeout=45.0) as client:
            resp = await client.post(f"{SCRAPER_URL}/collect", json=payload)
            print(f"Status Code: {resp.status_code}")
            if resp.status_code == 200:
                data = resp.json()
                error = data.get("error")
                count = data.get("count", 0)
                print(f"Count: {count}")
                if error:
                    print(f"Error field: {error}")
                if count > 0:
                    print(f"Sample item title: {data['items'][0].get('title') or data['items'][0].get('name')}")
                    print(f"Sample item URL: {data['items'][0].get('url')}")
            else:
                print(f"Response: {resp.text}")
    except Exception as e:
        print(f"Failed to query {source}: {e}")

async def main():
    # 1. Kannapedia by query
    await test_source({
        "source": "kannapedia",
        "query": "Qrazy Train",
        "limit": 3
    })
    
    # 2. Seedfinder (wait, seedfinder is run directly in python in cannabis-researcher, not in scraper-service, but let's check forum sources)
    
    # 3. Overgrow (discourse)
    await test_source({
        "source": "discourse",
        "base_url": "https://overgrow.com",
        "forum_name": "overgrow",
        "query": '"Qrazy Train"',
        "limit": 3
    })
    
    # 4. Rollitup (xenforo)
    await test_source({
        "source": "xenforo",
        "base_url": "https://www.rollitup.org",
        "forum_name": "rollitup",
        "query": '"Qrazy Train"',
        "limit": 3
    })
    
    # 5. THCFarmer (xenforo)
    await test_source({
        "source": "xenforo",
        "base_url": "https://www.thcfarmer.com",
        "forum_name": "thcfarmer",
        "query": '"Qrazy Train"',
        "limit": 3
    })
    
    # 6. ICMag (xenforo)
    await test_source({
        "source": "xenforo",
        "base_url": "https://www.icmag.com",
        "forum_name": "icmag",
        "query": '"Qrazy Train"',
        "limit": 3
    })

if __name__ == "__main__":
    asyncio.run(main())
