import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from modules.load_django import setup_django
from modules.bs4_parser import parse_brain_direct
from modules.selenium_parser import make_driver, search_and_parse
from modules.playwright_parser import main as playwright_main
import asyncio

if __name__ == "__main__":
    setup_django()

    print("🚀 RUNNING BS4 PARSER")
    data = parse_brain_direct(
        "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"
    )
    print(data)