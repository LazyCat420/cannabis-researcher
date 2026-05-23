import asyncio
from src.db import get_session
from sqlalchemy import select
from src.models.orm import GenomicSampleORM, CanonicalStrainORM, ChemicalProfileORM

async def run():
    session_gen = get_session()
    async for session in session_gen:
        # Find Canonical Strain for Head_Band or Headband
        res_strain = await session.execute(
            select(CanonicalStrainORM).where(
                (CanonicalStrainORM.primary_name == "Head_Band") | 
                (CanonicalStrainORM.primary_name == "HeadBand") |
                (CanonicalStrainORM.primary_name == "Headband")
            )
        )
        strains = res_strain.scalars().all()
        print(f"Found {len(strains)} Canonical Strain(s):")
        for s in strains:
            print(f"- ID: {s.id}, Name: {s.primary_name}, Avg THC: {s.avg_thc_pct}, Avg CBD: {s.avg_cbd_pct}, Dominant Terpenes: {s.dominant_terpenes}")
            
            # Find Genomic Samples for this strain
            res_samples = await session.execute(
                select(GenomicSampleORM).where(GenomicSampleORM.canonical_strain_id == s.id)
            )
            samples = res_samples.scalars().all()
            print(f"  Genomic Samples ({len(samples)}):")
            for sa in samples:
                print(f"  * RSP: {sa.rsp_number}, Name: {sa.sample_name}, Source URL: {sa.source_url}")
                
                # Find Chemical Profile
                res_cp = await session.execute(
                    select(ChemicalProfileORM).where(ChemicalProfileORM.sample_id == sa.id)
                )
                cp = res_cp.scalars().first()
                if cp:
                    print(f"    Chemical Profile: THC={cp.thc}, THCA={cp.thca}, CBD={cp.cbd}, CBDA={cp.cbda}")
        break

if __name__ == "__main__":
    asyncio.run(run())
