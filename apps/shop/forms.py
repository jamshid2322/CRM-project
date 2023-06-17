from django.forms import ModelForm
from django import forms
from apps.user.models import User
from apps.shop.models import ImportProduct, ShopProdcut , Product, Trade


class UserCreateForm(ModelForm):
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number')


    def save(self, commit=True):
    
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValueError("Password must match!!!")
        else:
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            user.save()
            return user
        

class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', "is_active" )
    
    def save(self):
        is_active = self.cleaned_data.get('is_active')
        is_deleted = self.instance.is_deleted
        if is_active and is_deleted:
            self.instance.is_deleted = False
        self.instance.save()
        return self.instance

class ProductImport(ModelForm):
    class Meta:
        model = ImportProduct
        fields = ('product', 'import_price', 'qty', 'shop' ,'sell_price', 'is_confirmed')

    def save(self):
        product = self.cleaned_data.get('product')
        shop = self.cleaned_data['shop']
        shop_product, _ = ShopProdcut.objects.get_or_create(product_id=product.id, shop_id=shop.id)
        shop_product.qty += self.cleaned_data['qty']
        shop_product.save()
        super().save()
        return self.instance
    
class ProductCreate(ModelForm):
    class Meta:
        model = Product
        fields =  ('title' , 'description' , 'category')

    def save(self):
        super().save()


class TradeCreateForm(forms.ModelForm):

    
    class Meta:
        model = Trade
        fields = ("shop", 'product', 'client', 'sold_price', 'qty')


class OrderProduct(forms.ModelForm):
    class Meta:
        model = ImportProduct
        fields = ('product', 'qty', 'shop')