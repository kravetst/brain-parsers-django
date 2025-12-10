from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time

URL = "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"

def make_driver():
    options = Options()
    options.add_argument("--headless")  # без GUI
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    return driver

def selenium_parse(url):
    driver = make_driver()
    driver.get(url)
    time.sleep(2)  # даємо час завантажитись скриптам

    scripts = driver.find_elements(By.XPATH, "//script[@type='application/ld+json']")
    product_data = None

    for script in scripts:
        try:
            data = json.loads(script.get_attribute("innerHTML"))
            if isinstance(data, list):
                for block in data:
                    if block.get("@type") == "Product":
                        product_data = block
                        break
            else:
                if data.get("@type") == "Product":
                    product_data = data
                    break
        except json.JSONDecodeError:
            continue
    driver.quit()

    if not product_data:
        return {"error": "Product JSON not found"}

    return {
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
        "link": url
    }

if __name__ == "__main__":
    result = selenium_parse(URL)
    print(result)
