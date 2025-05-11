import hashlib
import hmac
import time
import logging
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import TelegramUser

logger = logging.getLogger(__name__)

@api_view(["POST"])
def telegram_login(request):
    data = request.data
    received_hash = data.get("hash")
    auth_date = data.get("auth_date")

    # Step 1: Validate required parameters
    if not received_hash or not auth_date:
        return Response({"error": "Missing hash or auth_date"}, status=400)

    try:
        auth_date = int(auth_date)
    except ValueError:
        return Response({"error": "Invalid auth_date format"}, status=400)

    # Step 2: Check if authentication is expired (24 hours)
    if int(time.time()) - auth_date > 86400:
        return Response({"error": "Authentication expired."}, status=400)

    # Step 3: Prepare data for hash calculation (exclude the 'hash' key)
    auth_data = {k: v for k, v in data.items() if k != "hash"}
    sorted_data = sorted([f"{k}={v}" for k, v in auth_data.items()])
    data_check_string = "\n".join(sorted_data)

    # Step 4: Calculate the hash using HMAC with SHA-256
    secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    # Step 5: Verify if the calculated hash matches the received hash
    if calculated_hash != received_hash:
        return Response({"error": "Invalid data. Hash mismatch."}, status=400)

    # Step 6: Process the user login, create/update the user
    telegram_id = data.get("id")
    if not telegram_id:
        return Response({"error": "Missing Telegram user ID."}, status=400)

    telegram_user, _ = TelegramUser.objects.update_or_create(
        telegram_id=telegram_id,
        defaults={
            "username": data.get("username"),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "photo_url": data.get("photo_url", ""),
            "auth_date": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(auth_date)),
            "hash": received_hash,
        },
    )

    # Create or update the User object
    username = f"tg_{telegram_user.telegram_id}"
    user, _ = User.objects.get_or_create(username=username)

    # Optional: Prevent traditional login (Telegram only)
    if not user.has_usable_password():
        user.set_unusable_password()
        user.save()

    # Step 7: Generate JWT tokens
    refresh = RefreshToken.for_user(user)

    return Response({
        "message": "Authenticated",
        "telegram_id": telegram_user.telegram_id,
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
    })
