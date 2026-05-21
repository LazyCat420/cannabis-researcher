import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from src.db import get_session
from sqlalchemy import select
from src.models.orm import CanonicalStrainORM, StrainAliasORM, ObservationORM, ObservationImageORM

async def check():
    async for session in get_session():
        # Find Jacks Cleaner
        stmt = select(CanonicalStrainORM).where(CanonicalStrainORM.primary_name.ilike("%Jacks%"))
        strains = (await session.execute(stmt)).scalars().all()
        print(f"Strains matching 'Jacks': {len(strains)}")
        for s in strains:
            print(f"  - ID: {s.id}, Name: {s.primary_name}, Obs count: {s.observation_count}")
            # Count observations
            stmt_obs = select(ObservationORM).where(ObservationORM.canonical_strain_id == s.id)
            obss = (await session.execute(stmt_obs)).scalars().all()
            print(f"    - Database observations: {len(obss)}")
            # Let's count observation images
            for obs in obss:
                stmt_img = select(ObservationImageORM).where(ObservationImageORM.observation_id == obs.id)
                imgs = (await session.execute(stmt_img)).scalars().all()
                if imgs:
                    print(f"      - Observation {obs.id} has {len(imgs)} images:")
                    for img in imgs:
                        print(f"        - {img.image_url}")

        # Check aliases
        stmt_alias = select(StrainAliasORM).where(StrainAliasORM.source_id.ilike("%jacks-cleaner%"))
        aliases = (await session.execute(stmt_alias)).scalars().all()
        print(f"\nAliases matching 'jacks-cleaner': {len(aliases)}")
        for a in aliases:
            print(f"  - Name: {a.name}, Source ID: {a.source_id}, Canonical ID: {a.canonical_strain_id}")

if __name__ == "__main__":
    asyncio.run(check())
