import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    try:
        import cloudscraper
        scraper = cloudscraper.create_scraper()
        url = "https://seedfinder.eu/en/strain-info/Qrazy_Train/SubCools_The_Dank/"
        print(f"Fetching {url} using cloudscraper...")
        resp = scraper.get(url, timeout=15)
        print(f"Status Code: {resp.status_code}")
        content = resp.text
        print(f"Content length: {len(content)}")
        if "cloudflare" in content.lower() and resp.status_code == 403:
            print("Failed: cloudscraper was blocked")
        else:
            print("Success! Title check:")
            import re
            title = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
            if title:
                print(f"Title: {title.group(1)}")
            else:
                print("No title found, but not blocked")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
