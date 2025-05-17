import requests
from bs4 import BeautifulSoup
import json

def extract_json_ld(soup):
    json_ld_data = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string)
            json_ld_data.append(data)
        except Exception as e:
            continue
    return json_ld_data

def extract_microdata_rdfa(soup):
    microdata = []
    for tag in soup.find_all(True, attrs={"itemtype": True}):
        microdata.append({
            "tag": tag.name,
            "itemtype": tag.get("itemtype"),
            "itemscope": tag.has_attr("itemscope")
        })
    return microdata

def scrape_schema(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        print(f"\n🔗 URL: {url}")
        
        json_ld = extract_json_ld(soup)
        microdata = extract_microdata_rdfa(soup)

        if json_ld:
            print("\n📦 JSON-LD Detected:")
            for i, entry in enumerate(json_ld, 1):
                print(f"\nEntry {i}:\n{json.dumps(entry, indent=2)}")
        else:
            print("\n❌ No JSON-LD schema found.")

        if microdata:
            print("\n🏷️ Microdata / RDFa Detected:")
            for data in microdata:
                print(data)
        else:
            print("\n❌ No Microdata/RDFa schema found.")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    url = input("Enter the URL to check schema markup: ").strip()
    scrape_schema(url)
