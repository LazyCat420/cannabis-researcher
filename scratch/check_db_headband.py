import asyncio
import json
from sqlalchemy import select
from src.db import get_session
from src.models.orm import SourceGenomicsRecordORM

async def main():
    async for session in get_session():
        stmt = select(SourceGenomicsRecordORM)
        res = await session.execute(stmt)
        records = res.scalars().all()
        print("=== SOURCE GENOMICS RECORDS ===")
        for r in records:
            if "head" in str(r.payload).lower():
                print(f"ID: {r.id}, Sample ID: {r.genomic_sample_id}, Source ID: {r.source_id}")
                print("Payload:", json.dumps(r.payload, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
