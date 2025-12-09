from app.parser_app.models import Product
from django.db import IntegrityError

def save_product(data: dict, parser_tag: str):
    # choosing a key for uniqueness
    key = {}
    if data.get("sku"):
        key = {"sku": data["sku"]}
    else:
        key = {"link": data.get("link")}

    defaults = {
        "title": data.get("title"),
        "brand": data.get("brand"),
        "color": data.get("color"),
        "memory": data.get("memory"),
        "price": data.get("price"),
        "sale_price": data.get("sale_price"),
        "images": data.get("images") or [],
        "reviews_count": data.get("reviews_count"),
        "screen_diagonal": data.get("screen_diagonal"),
        "resolution": data.get("resolution"),
        "specs": data.get("specs") or {},
        "raw_jsonld": data.get("raw_jsonld"),
        "link": data.get("link"),
        "status": parser_tag,
    }
    try:
        product, created = Product.objects.update_or_create(**key, defaults=defaults)
        return product, created
    except IntegrityError as e:
        # to log or process
        raise