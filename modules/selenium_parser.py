import json
import re
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"

def parse_product_selenium(url: str) -> dict:
    # Set Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Launch Chrome
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # Try to get JSON-LD data
    try:
        script_tag = wait.until(EC.presence_of_element_located((By.XPATH, "//script[@type='application/ld+json']")))
        data = json.loads(script_tag.get_attribute("innerHTML"))
        product_data = None
        if isinstance(data, list):
            for item in data:
                if item.get("@type") == "Product":
                    product_data = item
                    break
        elif isinstance(data, dict) and data.get("@type") == "Product":
            product_data = data
    except:
        product_data = None

    # Extract fields from JSON-LD
    title = product_data.get("name") if product_data else None
    brand = (product_data.get("brand", {}).get("name") if isinstance(product_data.get("brand"), dict)
             else product_data.get("brand")) if product_data else None
    sku = product_data.get("sku") if product_data else None
    images = product_data.get("image", []) if product_data else []
    price = product_data.get("offers", {}).get("price") if product_data and product_data.get("offers") else None
    description = product_data.get("description", "") if product_data else ""

    # Extract color and memory from description
    color = None
    memory = None
    if description:
        desc_lower = description.lower()
        for c in ["чорний", "білий", "сірий", "коричневий"]:
            if c in desc_lower:
                color = c
                break
        mem_match = re.search(r"(\d{1,3}\s?gb)", description, re.IGNORECASE)
        if mem_match:
            memory = mem_match.group(1)

    # Fallback: extract missing fields from DOM
    if not title:
        try:
            title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.main-title"))).text
        except:
            title = None
    if not brand:
        try:
            brand = driver.find_element(By.CSS_SELECTOR, "div.brand a").text
        except:
            brand = None
    if not price:
        try:
            price_text = driver.find_element(By.CSS_SELECTOR, "span.price_value").text
            price = int(price_text.replace(" ", "").replace("₴", ""))
        except:
            price = None
    if not images:
        try:
            images = [img.get_attribute("href") for img in driver.find_elements(By.CSS_SELECTOR, "div.product-images a.fancybox")]
        except:
            images = []

    # Extract specifications
    specs = {}
    screen_diagonal = None
    resolution = None
    try:
        rows = driver.find_elements(By.CSS_SELECTOR, "div.product-characteristics table tr")
        for row in rows:
            try:
                key = row.find_element(By.TAG_NAME, "th").text.strip()
                value = row.find_element(By.TAG_NAME, "td").text.strip()
                specs[key] = value
                if "діагональ" in key.lower():
                    screen_diagonal = value
                if "роздільна здатність" in key.lower():
                    resolution = value
            except:
                continue
    except:
        pass

    # Close browser
    driver.quit()

    # Return product dictionary
    return {
        "title": title,
        "brand": brand,
        "color": color,
        "memory": memory,
        "price": price,
        "sku": sku,
        "images": images,
        "screen_diagonal": screen_diagonal,
        "resolution": resolution,
        "specs": specs,
        "link": url,
    }

# Save parsed data to JSON file
def save_to_json(data: dict):
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    file_path = results_dir / "selenium_products.json"

    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            saved = json.load(f)
    else:
        saved = []

    saved.append(data)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(saved, f, indent=2, ensure_ascii=False)

    print(f"✔ Saved to {file_path}")

# Test run
if __name__ == "__main__":
    data = parse_product_selenium(URL)
    print(data)
    save_to_json(data)
