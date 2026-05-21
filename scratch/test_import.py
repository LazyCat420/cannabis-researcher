import asyncio
import httpx
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

async def run_test():
    url = "http://localhost:8009"
    async with httpx.AsyncClient(timeout=30) as client:
        # 1. Search for Jack Herer
        logger.info("Testing search endpoint with query: Jack Herer")
        resp = await client.get(f"{url}/api/strains?search=Jack+Herer")
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        data = resp.json()
        strains = data.get("strains", [])
        
        logger.info(f"Found {len(strains)} search results.")
        seedfinder_strains = [s for s in strains if s.get("source") == "seedfinder"]
        logger.info(f"SeedFinder strains count: {len(seedfinder_strains)}")
        for s in seedfinder_strains[:3]:
            logger.info(f"  - {s['name']} (slug: {s['strain_slug']})")
            
        assert len(seedfinder_strains) > 0, "No SeedFinder strains returned!"
        
        # Take the first SeedFinder strain and import it
        target = seedfinder_strains[0]
        logger.info(f"Importing strain: {target['name']}")
        
        payload = {
            "strain_slug": target["strain_slug"],
            "breeder_slug": target["breeder_slug"]
        }
        
        import_resp = await client.post(f"{url}/api/strains/import", json=payload)
        assert import_resp.status_code == 200, f"Import failed with status {import_resp.status_code}: {import_resp.text}"
        
        detail = import_resp.json()
        logger.info("=== Import Successful ===")
        logger.info(f"Strain Name: {detail.get('name')}")
        logger.info(f"RSP: {detail.get('rsp')}")
        logger.info(f"Type: {detail.get('metadata', {}).get('plant_type') or detail.get('type')}")
        logger.info(f"Observations Count: {len(detail.get('observations', []))}")
        
        # Check that we got observations
        for obs in detail.get('observations', [])[:3]:
            logger.info(f"  - Observation by {obs.get('author')} from {obs.get('source_name')}: {obs.get('raw_text')[:100]}...")

if __name__ == "__main__":
    asyncio.run(run_test())
