

from multiprocessing import context
from tkinter.tix import Select
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from stocks.models import Wishlist, products
from category.models import category
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.http import HttpResponse
from django.db.models import Q
from . models import ProductGallery
# Create your views here. 
def stocks(request, category_slug=None):
    categories = None
    product = None
    if category_slug != None:
        categories = get_object_or_404(category, slug=category_slug)
        product = products.objects.filter(category=categories)
        paginator=Paginator(product,3)
        page = request.GET.get('page')
        paged_product =paginator.get_page(page)
        product_count = product.count()

    else:
        
        product = products.objects.all()
        paginator=Paginator(product,6)
        page = request.GET.get('page')
        paged_product =paginator.get_page(page)
        product_count = product.count()

    context = {'products': paged_product,
               'product_count':product_count,

               }

    return render(request, 'stocks/plans.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = products.objects.get(
            category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        
    except Exception as e:
        raise e
    
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'product_gallery': product_gallery,
    }
    return render(request, 'stocks/product-single.html', context)


@login_required(login_url = 'login')
def wishlist_add(request,id):
    data = Wishlist()
    user = request.user
    product = products.objects.get(id=id)
    wish = Wishlist.objects.filter(product=product,user=user).exists()
    print('pass')
    if not wish:
        
        product = products.objects.get(id=id)
        data.product = product
        data.user = user
        data.save()
    print('almost')
    return redirect('index')

@login_required(login_url ='login')
def wishlist(request):
    user=request.user
    productss=Wishlist.objects.filter(user=user)
    context = {
        'product':productss
    }
    return render(request,'stocks/wishlist.html',context)


@login_required(login_url = 'login')
def wishlist_remove(request,id):
    
    product=Wishlist.objects.get(id=id)
    product.delete()
    
    return redirect('wishlist')


def search(request):
  
    if request.method=='POST':
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        floors = request.POST.get('floors')
        parking = request.POST.get('parking')
        productsearchobj=products.objects.filter(Q(bedrooms=bedrooms),Q(bathrooms=bathrooms),Q(floors=floors),Q(parking=parking))
        return render(request,'stocks/plans.html',{'products':productsearchobj})
    else:
        productobj=products.objects.all()
    return render(request,'stocks/plans.html',{'products':productobj})