from django.contrib import admin
from django.urls import path, include
# from telegram_auth.views import get_jwt_token  # 👈 import the view properly

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/telegram/", include("telegram_auth.urls")),
    # path("api/token/", get_jwt_token),  # 👈 now this works
]
