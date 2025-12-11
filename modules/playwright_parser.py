import json
import re
import asyncio
from playwright.async_api import async_playwright

# Product page URL
URL = "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"

async def parse_product_playwright(url: str) -> dict:
    # Start Playwright context
    async with async_playwright() as p:
        # Launch headless Chromium browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        # Wait until main title is loaded (optional, 5s timeout)
        try:
            await page.wait_for_selector("h1.main-title", timeout=5000)
        except:
            pass  # Continue even if selector not found

        # Get full HTML content (not strictly needed here)
        html = await page.content()

        # Try to find JSON-LD scripts containing product info
        product_data = None
        try:
            scripts = await page.query_selector_all('script[type="application/ld+json"]')
            for script in scripts:
                content = await script.inner_text()
                try:
                    data = json.loads(content)
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
        except:
            pass

        # Extract fields from JSON-LD if available
        if product_data:
            title = product_data.get("name")
            brand = product_data.get("brand", {}).get("name")
            sku = product_data.get("sku")
            images = product_data.get("image", [])
            price = product_data.get("offers", {}).get("price")
            description = product_data.get("description", "")
        else:
            # Fallback: extract title from <h1> if JSON-LD not found
            try:
                title_elem = await page.query_selector("h1.main-title")
                title = await title_elem.text_content() if title_elem else None
            except:
                title = None
            brand = None
            sku = None
            images = []
            price = None
            description = ""

        # Extract color and memory from description/title
        color = None
        memory = None
        text_for_parse = description or title or ""
        text_lower = text_for_parse.lower()

        if "чорний" in text_lower:
            color = "чорний"
        elif "білий" in text_lower:
            color = "білий"
        elif "сірий" in text_lower:
            color = "сірий"
        elif "коричневий" in text_lower:
            color = "коричневий"

        mem_match = re.search(r"(\d{1,3}\s?gb)", text_lower)
        if mem_match:
            memory = mem_match.group(1)

        # Extract specifications from table
        specs = {}
        screen_diagonal = None
        resolution = None

        try:
            rows = await page.query_selector_all("div.product-characteristics table tr")
            for row in rows:
                try:
                    key_elem = await row.query_selector("th")
                    val_elem = await row.query_selector("td")
                    key = (await key_elem.text_content()).strip() if key_elem else None
                    value = (await val_elem.text_content()).strip() if val_elem else None
                    if key and value:
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
        await browser.close()

        # Return compact product dictionary
        return {
            "title": title,
            "brand": brand,
            "color": color,
            "memory": memory,
            "price": price,
            "sku": sku,
            "images": images,
            "specs": specs,
            "screen_diagonal": screen_diagonal,
            "resolution": resolution,
            "link": url,
        }

# Test run
if __name__ == "__main__":
    data = asyncio.run(parse_product_playwright(URL))
    print(data)
