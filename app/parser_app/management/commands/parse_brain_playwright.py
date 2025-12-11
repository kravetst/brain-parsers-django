import asyncio
import json
import csv
from pathlib import Path
from django.core.management import BaseCommand
from modules.playwright_parser import parse_product_playwright
from app.parser_app.services.save_product import save_product

URL = "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"

class Command(BaseCommand):
    help = "Parse product from Brain using Playwright and save to DB/JSON/CSV"

    def handle(self, *args, **options):
        self.stdout.write("Starting Brain Playwright Parser...")

        try:
            data = asyncio.run(parse_product_playwright(URL))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"Playwright parsing failed: {exc}"))
            return

        if not data or "error" in data:
            self.stdout.write(self.style.ERROR(data.get("error", "No data parsed")))
            return

        # ==== Save to DB ====
        try:
            product, created = save_product(data, parser_tag="playwright")
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added new product: {product.title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated product: {product.title}"))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f"Failed to save product: {exc}"))
            return

        # ==== Save JSON ====
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)

        json_file = results_dir / "playwright_data.json"
        if json_file.exists():
            with open(json_file, "r", encoding="utf-8") as f:
                saved = json.load(f)
        else:
            saved = []

        saved.append(data)
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(saved, f, indent=4, ensure_ascii=False)

        # ==== Save CSV ====
        csv_file = results_dir / "playwright_data.csv"
        file_exists = csv_file.exists()
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

        self.stdout.write(self.style.SUCCESS("Done! Saved Playwright data to DB + JSON + CSV"))