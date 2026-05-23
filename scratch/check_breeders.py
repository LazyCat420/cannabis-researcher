import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.db import get_session
from sqlalchemy import select
from src.models.orm import BreederORM, CanonicalStrainORM

async def run():
    session_gen = get_session()
    async for session in session_gen:
        res = await session.execute(select(BreederORM))
        breeders = res.scalars().all()
        print("Breeders in DB:")
        for b in breeders:
            print(f"- ID: {b.id}, Name: {b.name}")
            
        res_strains = await session.execute(
            select(CanonicalStrainORM).where(CanonicalStrainORM.primary_name.ilike("%qrazy%"))
        )
        strains = res_strains.scalars().all()
        for s in strains:
            print(f"\nStrain: {s.primary_name}, Breeder ID: {s.breeder_id}")
            
        break

if __name__ == "__main__":
    asyncio.run(run())
