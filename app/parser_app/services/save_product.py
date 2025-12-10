from django.db import IntegrityError
from app.parser_app.models import Product


def save_product(data: dict, parser_tag: str):
    """
    Save or update product in database.
    Uniqueness priority: SKU -> link.
    Returns tuple: (product_instance, is_created)
    """

    # Required data validation
    if not data.get("title") or not data.get("link"):
        raise ValueError("Product title and link are required fields")

    # Determine unique identifier
    lookup = {"sku": data["sku"]} if data.get("sku") else {"link": data.get("link")}

    # Prepare default update values
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
        "status": parser_tag,  # "brain", "foxtrot", "allo" etc.
    }

    try:
        product, created = Product.objects.update_or_create(
            **lookup,
            defaults=defaults
        )
        return product, created

    except IntegrityError as exc:
        # Better log instead of silent raise
        print(f"[DB ERROR] Failed to save product: {exc}")
        return None, False