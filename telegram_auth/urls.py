from django.urls import path
from .views import telegram_login , get_jwt_token

urlpatterns = [
    path("auth/", telegram_login, name="telegram_login"),
    
    path("jwt/", get_jwt_token, name="get_jwt_token"),
]
