from django.urls import path
from .views import (
    HomeInfoView,
    AboutUsView
    )

app_name = "info"
urlpatterns = [
    path('home-info', HomeInfoView.as_view(), name="home-info"),
    path('about-us', AboutUsView.as_view(), name="about-us"),
]
