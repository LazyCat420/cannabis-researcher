import asyncio
from sqlalchemy import select
from src.db import get_session
from src.models.orm import CanonicalStrainORM, GenomicSampleORM

async def main():
    async for session in get_session():
        res = await session.execute(select(GenomicSampleORM).where(GenomicSampleORM.canonical_strain_id == "8f4bec68-00ef-499a-b651-8cd8d11a2713"))
        samples = res.scalars().all()
        print(f"Genomic samples for Head_Band: {len(samples)}")
        for s in samples:
            print(s.rsp_number, s.strain_name)

if __name__ == "__main__":
    asyncio.run(main())
