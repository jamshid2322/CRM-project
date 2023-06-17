from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomManager(BaseUserManager):
    def create_user(self, first_name, last_name, role, phone_number, password, **extra_fields):
        if not first_name:
            raise ValueError("Error")
        if not last_name:
            raise ValueError("Error")
        if not role:
            raise ValueError("Error")
        if not password:
            raise ValueError("Error")
        if not phone_number:
            raise ValueError("Error")
        
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            role=role,
            phone_number=phone_number,
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, role, phone_number, password, **extra_fields):
        user = self.create_user(
            first_name, last_name, role, phone_number, password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user
    
