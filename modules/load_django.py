from pathlib import Path
import sys, os
import django


def setup_django():
    # Determine the project root directory (two levels up from this file: modules -> project root)
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Path to the "app" folder where brain_parsers_project (Django project) resides
    APP_DIR = BASE_DIR / "app"
    # Add the app directory to Python path, so Python can find Django project modules
    sys.path.append(str(APP_DIR))

    # Set the default Django settings module environment variable
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brain_parsers_project.settings")

    # Initialize Django (setup all apps, models, and settings)
    django.setup()