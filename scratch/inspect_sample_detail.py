import asyncio
import json
from src.db import get_session
from sqlalchemy import select
from src.models.orm import GenomicSampleORM

async def run():
    session_gen = get_session()
    async for session in session_gen:
        res = await session.execute(
            select(GenomicSampleORM).where(GenomicSampleORM.id == "d5b76b63-44d0-4aab-a3d9-eb506b40ac60")
        )
        sample = res.scalars().first()
        if sample:
            print("ID:", sample.id)
            print("RSP Number:", repr(sample.rsp_number))
            print("Strain Name:", sample.strain_name)
            print("Source URL:", sample.source_url)
            print("Raw Payload keys:", list(sample.raw_payload.keys()) if sample.raw_payload else None)
            print("Raw Payload:", json.dumps(sample.raw_payload, indent=2) if sample.raw_payload else None)
        else:
            print("Sample not found")
        break

if __name__ == "__main__":
    asyncio.run(run())
