from django.core.management.base import BaseCommand
from modules.bs4_parser import parse_product_bs4
from app.parser_app.services.save_product import save_product
import json
import csv
from pathlib import Path

class Command(BaseCommand):
    help = "Parse product from Brain using BS4 and save to DB/JSON/CSV"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Brain BS4 Parser...")

        data = parse_product_bs4()
        if not data:
            self.stdout.write(self.style.ERROR("No data parsed"))
            return

        # Save to DB
        product, created = save_product(data, parser_tag="bs4")
        if created:
            self.stdout.write(self.style.SUCCESS(f"Added new product: {product.title}"))
        else:
            self.stdout.write(self.style.WARNING(f"Updated product: {product.title}"))

        # Prepare results directory
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)

        # Save JSON
        json_file = results_dir / "bs4_data.json"
        if json_file.exists():
            with open(json_file, "r", encoding="utf-8") as f:
                saved = json.load(f)
        else:
            saved = []

        saved.append(data)
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(saved, f, indent=4, ensure_ascii=False)

        # Save CSV
        csv_file = results_dir / "bs4_data.csv"
        file_exists = csv_file.exists()
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

        self.stdout.write(self.style.SUCCESS("Done! Saved to DB + JSON + CSV"))

