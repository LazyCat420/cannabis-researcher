import asyncio
import httpx

async def test_bolinas():
    # 1. Search for Bolinas
    print("--- Testing /api/strains?search=Bolinas ---")
    async with httpx.AsyncClient() as client:
        r = await client.get("http://10.0.0.16:8005/api/strains?search=Bolinas", timeout=15.0)
        print("Status:", r.status_code)
        data = r.json()
        print("Data:", data)
        strains = data.get("strains", [])
        
        # We check if there's any strain with breeder_slug == 'forum-import'
        forum_import_strains = [s for s in strains if s.get("breeder_slug") == "forum-import"]
        if forum_import_strains:
            print("SUCCESS: Found forum import suggestion for Bolinas!")
            
            # 2. Try importing Bolinas
            print("\n--- Testing POST /api/strains/import for Bolinas ---")
            payload = {
                "strain_slug": "bolinas",
                "breeder_slug": "forum-import"
            }
            r_import = await client.post("http://10.0.0.16:8005/api/strains/import", json=payload, timeout=60.0)
            print("Import Status:", r_import.status_code)
            if r_import.status_code == 200:
                import_data = r_import.json()
                print("Import Data Name:", import_data.get("name"))
                print("Import Data Observations:", len(import_data.get("observations", [])))
            else:
                print("Import Failed:", r_import.text)
        else:
            print("FAILED: No forum import suggestion found for Bolinas.")

if __name__ == "__main__":
    asyncio.run(test_bolinas())
