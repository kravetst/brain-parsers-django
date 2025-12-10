from django.db import IntegrityError
from app.parser_app.models import Product

def save_product(data: dict, parser_tag: str):
    """
    Save or update a product in the database.
    Uniqueness priority: SKU -> link.
    Returns a tuple: (product_instance, is_created)
    """

    # Validate required fields
    if not data.get("title") or not data.get("link"):
        raise ValueError("Product title and link are required fields")

    # Determine unique identifier: use SKU if available, otherwise link
    lookup = {"sku": data["sku"]} if data.get("sku") else {"link": data.get("link")}

    # Prepare default values for update_or_create
    defaults = {
        "title": data.get("title"),
        "brand": data.get("brand"),
        "color": data.get("color"),
        "memory": data.get("memory"),
        "price": data.get("price"),
        "sale_price": data.get("sale_price"),
        "images": data.get("images") if data.get("images") else [],
        "reviews_count": data.get("reviews_count") or 0,
        "screen_diagonal": data.get("screen_diagonal"),
        "resolution": data.get("resolution"),
        "specs": data.get("specs") if data.get("specs") else {},
        # Limit raw_jsonld size to avoid extremely long text
        "raw_jsonld": (data.get("raw_jsonld")[:5000] if data.get("raw_jsonld") else None),
        "link": data.get("link"),
        "status": parser_tag,  # Indicates which parser/site this product comes from
    }

    try:
        # Save or update product in DB
        product, created = Product.objects.update_or_create(
            **lookup,
            defaults=defaults
        )
        return product, created

    except IntegrityError as exc:
        # Log DB error with product identifier
        identifier = data.get("sku") or data.get("link")
        print(f"[DB ERROR] Failed to save product {identifier}: {exc}")
        return None, False
