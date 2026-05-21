import asyncio
import httpx

async def check(url):
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(url + "/health")
            print(f"URL: {url} -> Status: {resp.status_code}, Body: {resp.text}")
    except Exception as e:
        print(f"URL: {url} -> Failed: {e}")

async def main():
    await check("http://localhost:8001")
    await check("http://10.0.0.16:8001")

if __name__ == "__main__":
    asyncio.run(main())
