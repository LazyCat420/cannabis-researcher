import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def check_db(url, label):
    print(f"--- Checking {label}: {url} ---")
    try:
        engine = create_async_engine(url)
        async with engine.connect() as conn:
            # Query canonical strains matching qrazy
            res = await conn.execute(text(
                "SELECT cs.id, cs.primary_name, cs.breeder_id, cs.lineage, b.name as breeder_name "
                "FROM canonical_strains cs "
                "LEFT JOIN breeders b ON cs.breeder_id = b.id "
                "WHERE cs.primary_name ILIKE :name"
            ), {"name": "%qrazy%"})
            rows = res.fetchall()
            print(f"Strains found ({len(rows)}):")
            for r in rows:
                print(f"- ID: {r[0]}, Name: {r[1]}, Breeder ID: {r[2]}, Breeder Name: {r[4]}")
                print(f"  Lineage: {r[3]}")
    except Exception as e:
        print(f"Connection failed: {e}")

async def main():
    # DB 1 (default fallback in code)
    await check_db(
        "postgresql+asyncpg://trader:trading_bot_pass@10.0.0.16:5433/trading_bot",
        "Port 5433"
    )
    # DB 2 (Vault projects.json config, but asyncpg needs postgresql+asyncpg://)
    await check_db(
        "postgresql+asyncpg://admin:password@10.0.0.16:5431/trading_bot",
        "Port 5431"
    )

if __name__ == "__main__":
    asyncio.run(main())
