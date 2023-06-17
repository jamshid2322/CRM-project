
from django.views.generic import View
from django.shortcuts import render
from apps.shop.models import Category, ImportProduct, ShopProdcut, Trade, User , Client , Product
from django.http import HttpResponseRedirect
from apps.shop.forms import ProductCreate, UserCreateForm, UserEditForm , ProductImport
from apps.utilis.permisions import UserAuthenticateRequiredMixin
import datetime
from django.db.models import Count, Sum, F
from django.db.models.functions import Cast, Coalesce

class CustomAdminView(UserAuthenticateRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        req_data = request.GET
        section = req_data.get("section")
        page = req_data.get('page')
        context = {
            'page': page
            
        }
        match page:
            case None | 'dashboard':
                filter_days = req_data.get('filter_day', 1)
                yesterday = datetime.date.today() - datetime.timedelta(days=int(filter_days))
                
                shops = User.objects.filter(role='shop').filter(shop_trade__created_at__gte=yesterday).annotate(
                    total_trading=Sum(F("shop_trade__sold_price")*F("shop_trade__qty"))
                )


                products = Product.objects.filter(shop_product__trade_product__created_at__gte=yesterday).annotate(
                    total_sum=Sum(F("shop_product__trade_product__sold_price") * F("shop_product__trade_product__qty")),
                    total_qty=Sum("shop_product__trade_product__qty")
                )

                context.update({
                    'shops_trade' : shops,
                    'products': products

                })








            case 'shop':
                shops = User.objects.filter(role="shop").order_by("-id")
                context.update({
                    'page': "shop",
                    'shops': shops, 
                })
            
            case "shop.create":
                context['page'] = page

            case "shop.edit":
                shop_id = req_data.get('shop_id')
                user_info = User.objects.get(id=shop_id)
                context.update({
                    'page': "shop.edit",
                    'user_info': user_info, 
                })

            case "shop.delete":
                shop_id = req_data.get('shop_id')
                user_info = User.objects.get(id=shop_id)
                context.update({
                    'page': "shop.delete",
                    'user_info': user_info, 
                })
            
            case 'shop.id':
                shop_id = req_data.get("shop_id")
                shop = User.objects.get(id=shop_id)
                trades = Trade.objects.filter(shop_id=shop_id)
                impoort_product = ShopProdcut.objects.filter(shop_id=shop_id)
                client = Client.objects.filter(shop_id=shop_id)
                section = req_data.get("section")
                user_infos = User.objects.all()
                products = Product.objects.all()

                context.update({
                    'page': 'shop.id',
                    'shop': shop,
                    "section": section,
                    "trades": trades,
                    "importproducts" : impoort_product,
                    "client" : client,
                    "user_infos" : user_infos,
                    "products" : products
                })
            
            case 'Products':
                product = Product.objects.all()
                context.update({
                    'product': product
                })
            

            case "shop.create.products":
                category = Category.objects.all()
                context['page'] = page
                context.update({
                   'category' : category
                    
                })

            case 'orders':
                match section:
                    case 'new.orders':
                        new_orders = ImportProduct.objects.filter(is_confirmed=False).order_by("-id")
                        context.update({
                            'section': section,
                            'new_orders': new_orders
                        })
                    case 'history.orders':
                        history_orders = ImportProduct.objects.filter(is_confirmed=True).order_by("-id")
                        context.update({
                            'section': section,
                            'history_orders': history_orders
                        })
                
        return render(request, 'custom_admin/index.html', context )


    def post(self, request, *args, **kwargs):
        method = request.POST.get("method")
        section = request.POST.get("section")
        req_data = request.POST
        match method:
            case "shop.create":
                form = UserCreateForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=True)
                    obj.role = 'shop'
                    obj.save()
                return HttpResponseRedirect("?page=shop")
            case "shop.edit":
                shop_id = req_data.get('shop_id')
                shop = User.objects.get(id=shop_id)
                form = UserEditForm(req_data, instance=shop)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('?page=shop')
                return HttpResponseRedirect(f'?page=shop.edit&shop_id={shop_id}')

            case "shop.dalete":
                shop_id = req_data.get('shop_id')
                shop = User.objects.get(id=shop_id) 
                shop.is_deleted = True
                shop.is_active = False
                shop.save()
                return HttpResponseRedirect('?page=shop')
            
            case "shop.id":
                shop_id = request.GET.get('shop_id')
                if section == 'Buyurtmalar':
                    form = ProductImport(request.POST)
                    if form.is_valid():
                        form.save()
                return HttpResponseRedirect(f'?page=shop.id&shop_id={shop_id}&section=Maxsulotlar')
            
            case "shop.create.products":
                form = ProductCreate(request.POST)
                form.save()
                return HttpResponseRedirect("?page=Products")
            
            
            case 'confirm.order':
                order = req_data.get('order_id')
                order_obj = ImportProduct.objects.get(id=order)
                form = ProductImport(req_data, instance=order_obj)
                if form.is_valid():
                    form.save()
                return HttpResponseRedirect(f'?page=orders&section=new.orders')


