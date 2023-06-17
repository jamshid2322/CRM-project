
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from apps import shop
from apps.shop.forms import OrderProduct, TradeCreateForm, UserCreateForm
from apps.shop.models import Client, Product, ShopProdcut, Trade
from apps.user.models import User
from apps.utilis.permisions import UserAuthenticateRequiredMixin
from django.contrib import messages

class CustomShopView(UserAuthenticateRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        shop = request.user
        req_data = request.GET
        page = req_data.get('page')
        section = req_data.get("section", "Savdo")
        context = {
            'page': page
            
        }
        match page:
            case None | 'shop':
                context

            case 'Products':
                product = Product.objects.all()
                
                context.update({
                        'product': product
                    })
            
            case 'shops':
                match section:
                    case 'Savdo':
                        clients = Client.objects.filter(shop_id=shop.id)
                        products = ShopProdcut.objects.filter(shop_id=shop.id).select_related('product', 'shop')
                        context.update({
                            "clients" : clients,
                            "products" : products,
                            'section': section
                        })
                    case 'Savdolar':
                        trades = Trade.objects.filter(shop_id=shop.id).select_related('shop', 'client', 'product')
                        context.update({
                            "trades" : trades,
                            'section': section
                        })
                    
                    case 'Maxsulotlar':
                        products = ShopProdcut.objects.filter(shop_id=shop.id).select_related('product', 'shop')
                        context.update({
                            "products" : products,
                            'section': section
                        })
                    case "Buyurtmalar":
                        products = Product.objects.all()
                        context.update({
                            'products': products,
                            'section': section
                        })
                    case 'Xaridorlar':
                        clients = Client.objects.filter(shop_id=shop.id).select_related("shop")
                        context.update({
                            'clients': clients,
                            'section': section
                        })
                
        return render(request, 'shops/indexshop.html', context )


    def post(self, request, *args, **kwargs):
        method = request.POST.get("method")
        page = request.POST.get("page", 'shops')
        section = request.POST.get("section", "Savdo")
        req_data = request.POST
        shop = request.user
        match method:
            case "trade.create":
                form = TradeCreateForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=True)
                    obj.shop = request.user

                    qty = obj.qty
                    shop_product = ShopProdcut.objects.filter(shop_id=obj.shop.id, product_id=obj.product.product.id).first()
                    if  shop_product.qty < qty:
                        messages.error(request, f"Maxsulot yetarli emas, qoldiq: {shop_product.qty}")
                    else:
                        shop_product.qty -= qty
                        shop_product.save()
                        obj.save()
                    # print(form.errors)
                return HttpResponseRedirect("?page=shops")
            
            case 'create.order':
                form = OrderProduct(req_data)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.shop = shop
                    obj.save()
                    return HttpResponseRedirect(f"?page=shops&section={section}")

            
           