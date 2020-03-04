from django.urls import path
from .views import (
    HomeView, 
    ShopView, 
    ProductsList,
    ProductDetailView,
    VariantDetail
    )

app_name = "shop"
urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('shop/', ShopView.as_view(), name="store"),
    path('shop/products', ProductsList.as_view(), name="products-list"),
    path('shop/product/<int:product_variant_id>/', ProductDetailView.as_view(), name="product-detail"),
    path('shop/product-varient/<int:product_variant_id>/', VariantDetail.as_view(), name="variant-detail")
]
