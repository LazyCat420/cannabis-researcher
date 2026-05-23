import re

def parse_genetics_from_snippets(snippets, strain_name):
    # Normalize strain name
    name_norm = re.sub(r'[^a-zA-Z0-9]', '', strain_name.lower())
    
    # Try different regex strategies across all snippets
    for snip in snippets:
        snip_clean = snip.replace('\xa0', ' ').replace('\u200e', '')
        print(f"\nAnalyzing snippet: {snip_clean[:100]}...")
        
        # Strategy 1: Look for "StrainName »»» Parent1 x Parent2" or "Strain Name »»» Parent1 x Parent2"
        match = re.search(r'»»»\s*([^·\n]+)', snip_clean)
        if match:
            cross_text = match.group(1).strip()
            print(f"  Strategy 1 matched: {cross_text}")
            if any(x in cross_text.lower() for x in [' x ', '×', ' x']):
                parts = re.split(r'\s+[xX×]\s+|\s+x\s+|_x_|_X_', cross_text)
                parents = [p.strip() for p in parts if p.strip()]
                parents = [p for p in parents if len(p) > 2 and p.lower() not in ["mostly indica", "mostly sativa", "hybrid"]]
                if len(parents) >= 2:
                    return parents
                    
        # Strategy 2: Look for "Genetic:Parent1 x Parent2 x Parent3"
        match_genetic = re.search(r'Genetic\s*:\s*([^.\n]+)', snip_clean, re.IGNORECASE)
        if match_genetic:
            cross_text = match_genetic.group(1).strip()
            cross_text = re.split(r'flowering|characteristics|strong|medicinal', cross_text, flags=re.IGNORECASE)[0].strip()
            print(f"  Strategy 2 matched: {cross_text}")
            if any(x in cross_text.lower() for x in [' x ', '×', ' x']):
                parts = re.split(r'\s+[xX×]\s+|\s+x\s+|_x_|_X_', cross_text)
                parents = [p.strip() for p in parts if p.strip()]
                parents = [p for p in parents if len(p) > 2 and p.lower() not in ["mostly indica", "mostly sativa", "hybrid"]]
                if len(parents) >= 2:
                    return parents
                    
        # Strategy 3: Heuristic for Capitalized Words separated by 'x'
        for match in re.finditer(r'([A-Z][a-zA-Z0-9\s\']+)\s+[xX×*]\s+([A-Z][a-zA-Z0-9\s\']+)(?:\s+[xX×*]\s+([A-Z][a-zA-Z0-9\s\']+))?', snip_clean):
            parents = [p.strip() for p in match.groups() if p]
            parents = [p for p in parents if len(p) > 2 and p.lower() not in ["mostly indica", "mostly sativa", "hybrid"] and len(p) < 40]
            print(f"  Strategy 3 matched: {parents}")
            if len(parents) >= 2:
                return parents

    return []

def main():
    snippets = [
        "Here you can browse the lineage tree · Qrazy Train »»» Blood Wreck x Querkle · »»» Blood Wreck x Querkle · Blood Wreck · »»» Trainwreck x Trinity · Trainwreck · USA »»» Unknown Hybrid · Trinity (3-way hybrid) »»» USA, Kalifornien · Querkle · »»» Urkle x Space Queen ·",
        "Independent, standardized information about SubCool’s The Dank cannabis-strain Qrazy Train! Find phenotypes, comments + detailed profiles, flowering-time, THC-Content, images, prices & stores, extended family-tree & lineages, crossings & hybrids, grow-journals, direct-comparisons, medicinal properties, and much more!",
        "Genetic:Train Wreck x Trinity x QuerkleFlowering time: 8 weeks Characteristics: Strong and pleasant high, very good for pain relief and relaxation. Good for treating body pain. ... Click to show all parents of Qrazy Train in our dynamic family ...",
        "Click and Zoom into all ancestors of the marijuana strain Qrazy Train from the cannabis breeder SubCool’s The Dank with the help of SeedFinders unique, amazing and dynamic family tree!",
        "Type: Hybrid indica/sativa Sex: Regular F2 Genetics:Hybrid: Qrazy Train (Black Trainwreck x Trinity x Purple Urkle x Space Queen) x Cheese Quake (Exodus Cheese x Querkle)Flowering Time: 9 weeks Outdoor Harvest: Sept/Oct Height: Medium THC ..."
    ]
    parents = parse_genetics_from_snippets(snippets, "Qrazy Train")
    print(f"\nFinal parsed parents: {parents}")

if __name__ == "__main__":
    main()
