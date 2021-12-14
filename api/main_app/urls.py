from django.urls import path

from .views import TelegramUserCreate, CitymobilRedirectView, MaximRedirectView


app_name = 'main_app'

urlpatterns = [
    path('citymobil/', CitymobilRedirectView.as_view()),
    path('maxim/', MaximRedirectView.as_view()),

    path('api/v1/telegram_user/', TelegramUserCreate.as_view())
]
