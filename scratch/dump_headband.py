import asyncio
from sqlalchemy import select
from src.db import get_session
from src.models.orm import CanonicalStrainORM, StrainAliasORM, GenomicSampleORM

async def main():
    async for session in get_session():
        # Get strains
        strains = (await session.execute(select(CanonicalStrainORM))).scalars().all()
        print("=== ALL CANONICAL STRAINS ===")
        for s in strains:
            if "head" in s.primary_name.lower():
                print(f"Strain ID: {s.id}, Name: {s.primary_name}, Breeder ID: {s.breeder_id}")
                
        # Get aliases
        aliases = (await session.execute(select(StrainAliasORM))).scalars().all()
        print("\n=== ALL STRAIN ALIASES ===")
        for a in aliases:
            if "head" in a.name.lower() or "head" in (a.source_id or "").lower():
                print(f"Alias ID: {a.id}, Canonical ID: {a.canonical_strain_id}, Name: {a.name}, Source: {a.source_name}, Source ID: {a.source_id}")
                
        # Get genomic samples
        samples = (await session.execute(select(GenomicSampleORM))).scalars().all()
        print("\n=== ALL GENOMIC SAMPLES ===")
        for s in samples:
            if "head" in s.strain_name.lower() or "head" in (s.rsp_number or "").lower():
                print(f"Sample ID: {s.id}, Canonical ID: {s.canonical_strain_id}, Strain Name: {s.strain_name}, RSP: {s.rsp_number}")

if __name__ == "__main__":
    asyncio.run(main())
