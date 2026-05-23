import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.db import get_session
from sqlalchemy import select
from src.models.orm import CanonicalStrainORM, GenomicSampleORM

async def run():
    session_gen = get_session()
    async for session in session_gen:
        res = await session.execute(select(CanonicalStrainORM))
        strains = res.scalars().all()
        print(f"Total Canonical Strains in DB: {len(strains)}")
        for s in strains:
            res_gen = await session.execute(
                select(GenomicSampleORM).where(GenomicSampleORM.canonical_strain_id == s.id)
            )
            gens = res_gen.scalars().all()
            print(f"- Name: {s.primary_name}, ObsCount: {s.observation_count}, Genomic Samples: {len(gens)} (RSPs: {[g.rsp_number for g in gens]})")
        break

if __name__ == "__main__":
    asyncio.run(run())
