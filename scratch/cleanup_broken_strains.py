import asyncio
from sqlalchemy import select, delete
from src.db import get_session
from src.models.orm import CanonicalStrainORM, StrainAliasORM, ObservationORM, ObservationImageORM, GenomicSampleORM, ChemicalProfileORM, GeneticRelationshipORM, SourceGenomicsRecordORM

async def main():
    print("Connecting to DB and searching for malformed strains...")
    async for session in get_session():
        # Find malformed strains containing "page_not_found" or "<title" or "Page_not_found"
        stmt = select(CanonicalStrainORM).where(
            (CanonicalStrainORM.primary_name.like("%page_not_found%")) |
            (CanonicalStrainORM.primary_name.like("%Page_not_found%")) |
            (CanonicalStrainORM.primary_name.like("%<title%")) |
            (CanonicalStrainORM.primary_name.like("%html%"))
        )
        broken_strains = (await session.execute(stmt)).scalars().all()
        if not broken_strains:
            print("No malformed strains found in DB.")
            return

        print(f"Found {len(broken_strains)} malformed strain(s) to clean up:")
        for strain in broken_strains:
            print(f" - ID: {strain.id}, Name: {strain.primary_name[:100]}...")

            # Clean up observations and images
            obs_stmt = select(ObservationORM.id).where(ObservationORM.canonical_strain_id == strain.id)
            obs_ids = (await session.execute(obs_stmt)).scalars().all()
            if obs_ids:
                print(f"   * Deleting {len(obs_ids)} observations and their images")
                await session.execute(delete(ObservationImageORM).where(ObservationImageORM.observation_id.in_(obs_ids)))
                await session.execute(delete(ObservationORM).where(ObservationORM.id.in_(obs_ids)))

            # Clean up genomic samples, chemical profiles, relationships
            gs_stmt = select(GenomicSampleORM).where(GenomicSampleORM.canonical_strain_id == strain.id)
            gs_records = (await session.execute(gs_stmt)).scalars().all()
            for gs in gs_records:
                print(f"   * Deleting GenomicSample {gs.rsp_number}")
                if gs.chemical_profile_id:
                    await session.execute(delete(ChemicalProfileORM).where(ChemicalProfileORM.id == gs.chemical_profile_id))
                await session.execute(delete(GeneticRelationshipORM).where((GeneticRelationshipORM.genomic_sample_id == gs.id) | (GeneticRelationshipORM.rsp_b == gs.rsp_number)))
                await session.execute(delete(SourceGenomicsRecordORM).where(SourceGenomicsRecordORM.genomic_sample_id == gs.id))
                await session.execute(delete(GenomicSampleORM).where(GenomicSampleORM.id == gs.id))

            # Delete aliases
            aliases_deleted = await session.execute(delete(StrainAliasORM).where(StrainAliasORM.canonical_strain_id == strain.id))
            print(f"   * Deleted {aliases_deleted.rowcount} aliases")

            # Delete the strain itself
            await session.delete(strain)
            print(f"   * Deleted strain {strain.id}")

        await session.commit()
        print("Cleanup completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
