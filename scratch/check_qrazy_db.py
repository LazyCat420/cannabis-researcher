import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.db import get_session
from sqlalchemy import select
from src.models.orm import CanonicalStrainORM, StrainAliasORM, GenomicSampleORM, ObservationORM

async def run():
    session_gen = get_session()
    async for session in session_gen:
        # 1. Search Canonical Strains
        res_strains = await session.execute(
            select(CanonicalStrainORM)
        )
        strains = res_strains.scalars().all()
        print(f"All Canonical Strains ({len(strains)}):")
        for s in strains:
            from src.models.orm import BreederORM
            breeder_name = "Unknown"
            if s.breeder_id:
                res_b = await session.execute(select(BreederORM).where(BreederORM.id == s.breeder_id))
                b = res_b.scalars().first()
                if b:
                    breeder_name = b.name
            print(f"- ID: {s.id}, Name: {s.primary_name}, Breeder: {breeder_name} ({s.breeder_id}), Type: {s.strain_type}, Flow: {s.avg_flowering_days}, ObsCount: {s.observation_count}")
            print(f"  Lineage: {s.lineage}")
            
            # Find aliases for this strain
            res_aliases = await session.execute(
                select(StrainAliasORM).where(StrainAliasORM.canonical_strain_id == s.id)
            )
            aliases = res_aliases.scalars().all()
            print(f"  Aliases ({len(aliases)}):")
            for a in aliases:
                print(f"    * Name: {a.name}, Source: {a.source_name}, Source ID: {a.source_id}")
                
            # Find observations
            res_obs = await session.execute(
                select(ObservationORM).where(ObservationORM.canonical_strain_id == s.id)
            )
            obs = res_obs.scalars().all()
            print(f"  Observations ({len(obs)}):")
            for o in obs[:5]:
                print(f"    * Author: {o.author}, Source: {o.source_name}, Url: {o.source_url}, Text len: {len(o.raw_text) if o.raw_text else 0}")
                
            # Find genomic samples
            res_gen = await session.execute(
                select(GenomicSampleORM).where(GenomicSampleORM.canonical_strain_id == s.id)
            )
            gens = res_gen.scalars().all()
            print(f"  Genomic Samples ({len(gens)}):")
            for g in gens:
                print(f"    * RSP: {g.rsp_number}, Name: {g.sample_name}, Source: {g.source}")
                
        break

if __name__ == "__main__":
    asyncio.run(run())
