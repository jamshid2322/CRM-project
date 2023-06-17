from django.contrib import admin
from apps.shop.models import (
    Product,
    ProductImage,
    Category,
    Client,
    ImportProduct,
    Trade,
    ShopProdcut
)
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent')
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id' , 'title' , 'category')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id' , 'product')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'shop', 'created_at')

@admin.register(ImportProduct)
class ImportProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'import_price', 'qty', 'shop', 'sell_price', 'is_confirmed')

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'product', 'client', 'sold_price', 'qty', 'created_at')

@admin.register(ShopProdcut)
class ShopProdcutAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'qty', 'shop')