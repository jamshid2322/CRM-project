import datetime
from django.db import models
from apps.user.models import User


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13)
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.shop.first_name


class Category(models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True , blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.product.title


class ImportProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    import_price = models.PositiveIntegerField(blank=True, null=True)
    qty = models.PositiveBigIntegerField()
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sell_price = models.PositiveIntegerField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    
class ShopProdcut(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='shop_product')
    qty = models.PositiveBigIntegerField(default=0)
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Trade(models.Model):
    shop = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True , related_name='shop_trade')
    product = models.ForeignKey(ShopProdcut, on_delete=models.SET_NULL, null=True, related_name='trade_product')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    sold_price = models.PositiveIntegerField()
    qty = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self , *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.date.today()
        super().save(*args, **kwargs)
