from django.urls import path
from .views import UserRegisterLogin


urlpatterns = [
    path('login/', UserRegisterLogin.as_view(), name='register_login'),
    path('logout/', UserRegisterLogin.as_view(), name='logout')
]

