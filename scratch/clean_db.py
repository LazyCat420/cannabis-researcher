import asyncio
from src.db import get_session
from sqlalchemy import select, delete
from src.models.orm import GenomicSampleORM, ChemicalProfileORM, GeneticRelationshipORM, SourceGenomicsRecordORM

async def run():
    session_gen = get_session()
    async for session in session_gen:
        # Find sample
        res = await session.execute(
            select(GenomicSampleORM).where(GenomicSampleORM.id == "d5b76b63-44d0-4aab-a3d9-eb506b40ac60")
        )
        sample = res.scalars().first()
        if not sample:
            print("Invalid sample not found in DB.")
            break
            
        print("Found invalid sample:", sample.id, repr(sample.rsp_number), sample.strain_name)
        
        # Check chemical profile
        res_cp = await session.execute(
            select(ChemicalProfileORM).where(ChemicalProfileORM.sample_id == sample.id)
        )
        cps = res_cp.scalars().all()
        print(f"Related chemical profiles count: {len(cps)}")
        for cp in cps:
            await session.delete(cp)
            
        # Check genetic relationships
        res_gr = await session.execute(
            select(GeneticRelationshipORM).where(GeneticRelationshipORM.sample_id_a == sample.id)
        )
        grs = res_gr.scalars().all()
        print(f"Related genetic relationships count: {len(grs)}")
        for gr in grs:
            await session.delete(gr)
            
        # Check source genomics records
        res_sg = await session.execute(
            select(SourceGenomicsRecordORM).where(SourceGenomicsRecordORM.genomic_sample_id == sample.id)
        )
        sgs = res_sg.scalars().all()
        print(f"Related source genomics records count: {len(sgs)}")
        for sg in sgs:
            await session.delete(sg)
            
        # Delete sample itself
        await session.delete(sample)
        print("Sample and related records deleted from session.")
        
        await session.commit()
        print("Database commit successful.")
        break

if __name__ == "__main__":
    asyncio.run(run())
