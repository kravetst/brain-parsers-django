import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path


URL = "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"


def parse_product_bs4() -> dict:
    """
    Parse product information using BeautifulSoup and return structured data.
    If some values are missing — return None instead.
    """

    response = requests.get(URL, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })

    soup = BeautifulSoup(response.text, "html.parser")

    scripts = soup.find_all("script", type="application/ld+json")
    product_data = None

    # Extract JSON-LD block with product details (sometimes list, sometimes dict)
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

    # Form a result structure
    result = {
        "name": product_data.get("name"),
        "price": product_data.get("offers", {}).get("price"),
        "currency": product_data.get("offers", {}).get("priceCurrency"),
        "in_stock": product_data.get("offers", {}).get("availability"),
        "images": product_data.get("image", []),
        "brand": product_data.get("brand", {}).get("name"),
        "rating": product_data.get("aggregateRating", {}).get("ratingValue"),
        "reviews_count": product_data.get("aggregateRating", {}).get("reviewCount"),
        "sku": product_data.get("sku"),
        "mpn": product_data.get("mpn"),
        "description": product_data.get("description"),
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

    # If file exists — load and append, else create with array
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