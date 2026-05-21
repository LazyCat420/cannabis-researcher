#!/usr/bin/env python3
import asyncio
import logging
from sqlalchemy import select
from src.db import init_db, get_session
from src.models.orm import ObservationImageORM
from src.ml.clustering import is_budding_plant_image

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("purge_images")

async def main():
    logger.info("Initializing database connection...")
    await init_db()
    
    async for session in get_session():
        stmt = select(ObservationImageORM)
        images = (await session.execute(stmt)).scalars().all()
        logger.info(f"Loaded {len(images)} images from the database.")
        
        purged_count = 0
        for img in images:
            logger.info(f"Checking image {img.id}: {img.image_url}")
            is_valid = await is_budding_plant_image(img.image_url)
            if not is_valid:
                logger.info(f"Purging non-budding image {img.id}: {img.image_url}")
                await session.delete(img)
                purged_count += 1
            
        if purged_count > 0:
            await session.commit()
            logger.info(f"Successfully purged {purged_count} non-budding images.")
        else:
            logger.info("No images needed to be purged.")
        break

if __name__ == "__main__":
    asyncio.run(main())
