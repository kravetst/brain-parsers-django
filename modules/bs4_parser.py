import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

URL = "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"

def parse_product_bs4() -> dict:
    """
    Parse product information using BeautifulSoup.
    Returns only the required fields in a compact structure.
    """

    # Send request
    response = requests.get(URL, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })
    soup = BeautifulSoup(response.text, "lxml")

    # Extract JSON-LD scripts
    scripts = soup.find_all("script", type="application/ld+json")
    product_data = None

    # Find product JSON-LD
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, list):
                for item in data:
                    if item.get("@type") == "Product":
                        product_data = item
                        break
            elif data.get("@type") == "Product":
                product_data = data
                break
        except:
            continue

    if not product_data:
        return {"error": "Product JSON not found"}

    # Extract basic fields
    title = product_data.get("name")
    brand = product_data.get("brand", {}).get("name")
    sku = product_data.get("sku")
    images = product_data.get("image", [])
    price = product_data.get("offers", {}).get("price")
    sale_price = product_data.get("offers", {}).get("price")  # Modify if site has discount
    reviews_count = product_data.get("aggregateRating", {}).get("reviewCount")

    # Extract description to parse color and memory
    description = product_data.get("description", "")
    color = None
    memory = None
    if description:
        # Example: "256 Gb, чорний"
        if "чорний" in description.lower():
            color = "чорний"
        elif "білий" in description.lower():
            color = "білий"
        elif "сірий" in description.lower():
            color = "сірий"
        elif "коричневий" in description.lower():
            color = "коричневий"

        import re
        mem_match = re.search(r"(\d{1,3}\s?Gb)", description, re.IGNORECASE)
        if mem_match:
            memory = mem_match.group(1)

    # Extract screen info and specs
    screen_diagonal = None
    resolution = None
    specs = {}

    specs_table = soup.select("div.product-characteristics table tr")
    for row in specs_table:
        try:
            key = row.find("th").get_text(strip=True)
            value = row.find("td").get_text(strip=True)
            specs[key] = value
            if "діагональ" in key.lower():
                screen_diagonal = value
            if "роздільна здатність" in key.lower():
                resolution = value
        except:
            continue

    # Build final compact dictionary
    result = {
        "title": title,
        "brand": brand,
        "color": color,
        "memory": memory,
        "price": price,
        "sale_price": sale_price,
        "images": images,
        "sku": sku,
        "reviews_count": reviews_count,
        "screen_diagonal": screen_diagonal,
        "resolution": resolution,
        "specs": specs,
        "link": URL,
    }

    return result


def save_to_json(data: dict):
    """
    Save parsed product data into ./results/bs4_products.json
    Creates file if missing, appends object if exists.
    """

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    file_path = results_dir / "bs4_products.json"

    # Load existing file or create new
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            saved = json.load(file)
    else:
        saved = []

    saved.append(data)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(saved, file, indent=2, ensure_ascii=False)

    print(f"✔ Saved to {file_path}")


if __name__ == "__main__":
    data = parse_product_bs4()
    print(data)
    save_to_json(data)