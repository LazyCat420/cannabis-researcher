import asyncio
from src.db import get_session
from sqlalchemy import select
from src.models.orm import GenomicSampleORM

async def run():
    session_gen = get_session()
    async for session in session_gen:
        res = await session.execute(
            select(GenomicSampleORM).where(GenomicSampleORM.rsp_number == "")
        )
        samples = res.scalars().all()
        print(f"Total samples with empty rsp_number: {len(samples)}")
        for s in samples:
            print(f"ID: {s.id}, Strain: {s.strain_name}, Source: {s.source}, Source URL: {s.source_url}")
        break

if __name__ == "__main__":
    asyncio.run(run())
