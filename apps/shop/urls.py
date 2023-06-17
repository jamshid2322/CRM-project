from django.urls import path
from apps.shop.view import (
    custom_admin,
    home,
    shop
)

urlpatterns = [
    path("", home.home, name="home"),
    path('dashboard/', custom_admin.CustomAdminView.as_view(), name='custom_admin'),
    path('shop/', shop.CustomShopView.as_view(), name='shop')
]