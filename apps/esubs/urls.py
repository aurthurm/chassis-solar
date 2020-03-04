from django.urls import path
from .views import (
    SubscribeView,
    )

app_name = "esubs"
urlpatterns = [
    path('subscribe', SubscribeView.as_view(), name="subscribe"),
]
