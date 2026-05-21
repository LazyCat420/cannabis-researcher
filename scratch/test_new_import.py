import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
import httpx
from src.db import get_session
from sqlalchemy import select, delete
from src.models.orm import CanonicalStrainORM, StrainAliasORM, ObservationORM, ObservationImageORM

async def run_test():
    print("=== Clean-slate Import Test ===")
    
    # 1. Clear existing database records for Jacks Cleaner
    async for session in get_session():
        # Find the canonical strain first
        stmt = select(CanonicalStrainORM).where(CanonicalStrainORM.primary_name.ilike("%Jacks%"))
        strains = (await session.execute(stmt)).scalars().all()
        for s in strains:
            print(f"Deleting existing records for strain ID: {s.id} ({s.primary_name})")
            
            # Find and delete observation images
            stmt_obs = select(ObservationORM).where(ObservationORM.canonical_strain_id == s.id)
            obss = (await session.execute(stmt_obs)).scalars().all()
            for obs in obss:
                await session.execute(delete(ObservationImageORM).where(ObservationImageORM.observation_id == obs.id))
                
            # Delete observations
            await session.execute(delete(ObservationORM).where(ObservationORM.canonical_strain_id == s.id))
            
            # Delete aliases
            await session.execute(delete(StrainAliasORM).where(StrainAliasORM.canonical_strain_id == s.id))
            
            # Delete canonical strain
            await session.execute(delete(CanonicalStrainORM).where(CanonicalStrainORM.id == s.id))
            
        await session.commit()
        print("Existing Jacks Cleaner records cleared.")

    # 2. Call the import API on NAS production server (port 8005)
    print("\nSending import request to NAS production server (http://10.0.0.16:8005)...")
    payload = {
        "strain_slug": "jacks-cleaner",
        "breeder_slug": "subcools-the-dank"
    }
    
    async with httpx.AsyncClient(timeout=180.0) as client:
        try:
            resp = await client.post("http://10.0.0.16:8005/api/strains/import", json=payload)
            if resp.status_code != 200:
                print(f"Import failed: HTTP {resp.status_code} - {resp.text}")
                return
            
            detail = resp.json()
            print("\n=== Import Completed Successfully ===")
            print(f"Name: {detail.get('name')}")
            print(f"Type: {detail.get('strain_type') or detail.get('type')}")
            print(f"Breeder: {detail.get('breeder')}")
            print(f"Lineage count: {len(detail.get('lineage', {}))}")
        except Exception as e:
            print(f"API Request failed: {e}")
            return

    # 3. Check the database to see what was inserted
    print("\n--- Verification: Checking Database for Grow Logs & Images ---")
    async for session in get_session():
        stmt = select(CanonicalStrainORM).where(CanonicalStrainORM.primary_name.ilike("%Jacks%"))
        strains = (await session.execute(stmt)).scalars().all()
        for s in strains:
            # Check observations
            stmt_obs = select(ObservationORM).where(ObservationORM.canonical_strain_id == s.id)
            obss = (await session.execute(stmt_obs)).scalars().all()
            print(f"Saved observations: {len(obss)}")
            for idx, obs in enumerate(obss):
                print(f"\n[{idx+1}] Observation by {obs.author} from {obs.source_name}:")
                print(f"    URL: {obs.source_url}")
                print(f"    Body snippet: {obs.raw_text[:200].replace('\n', ' ')}...")
                
                # Fetch images for this observation
                stmt_img = select(ObservationImageORM).where(ObservationImageORM.observation_id == obs.id)
                imgs = (await session.execute(stmt_img)).scalars().all()
                if imgs:
                    print(f"    Images ({len(imgs)}):")
                    for img in imgs:
                        print(f"      - {img.image_url}")

if __name__ == "__main__":
    asyncio.run(run_test())
