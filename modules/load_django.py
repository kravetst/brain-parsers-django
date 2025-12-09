from pathlib import Path
import sys, os
import django

def setup_django():
    BASE_DIR = Path(__file__).resolve().parent.parent  # modules -> корінь
    APP_DIR = BASE_DIR / "app"                          # app, де лежить brain_parsers_project
    sys.path.append(str(APP_DIR))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brain_parsers_project.settings")
    django.setup()