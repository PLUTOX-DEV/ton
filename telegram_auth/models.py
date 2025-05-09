# telegram_auth/models.py

from django.db import models

class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)
    auth_date = models.DateTimeField()
    hash = models.CharField(max_length=255)

    def __str__(self):
        return self.username or str(self.telegram_id)
