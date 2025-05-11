import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")  # replace with your project name
django.setup()

from django.conf import settings

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
