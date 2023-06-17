from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser

from .managers import CustomManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE = (
        ('admin', 'admin'),
        ('shop', 'shop'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13, unique=True)
    role = models.CharField(max_length=6, choices=ROLE)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", 'last_name', 'role']

    objects = CustomManager()
    
    def __str__(self):
        return self.phone_number


