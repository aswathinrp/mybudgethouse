from gc import get_objects
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
import razorpay
from accounts.forms import RegistrationForm, UserProfileForm
from accounts.models import Accounts
from stocks.models import products
from django.http import HttpResponse
from .models import Cart, CartItem
from .forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
import razorpay
from django.conf import settings
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, products_id):
    current_user = request.user
    product= products.objects.get(id=products_id)
    if current_user.is_authenticated:
        
        try:
            cart_item = CartItem.objects.get(product=product,user=current_user)
            cart_item.quantity += 1
            cart_item.save()
        
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=request.user,
            )
            cart_item.save()
        return redirect('cart')
   
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
      
        try:
            cart_item = CartItem.objects.get(product=product,cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        
        except CartItem.DoesNotExist:
            print(product,cart,request.user)
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart, 
            )
            cart_item.save()
        return redirect('cart')
   

def remove_cart(request, products_id, cart_item_id):
    product = get_object_or_404(products, id=products_id)
    try:
        if request.user.is_authenticated:
             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
                cart_item.quantity -=1
                cart_item.save()
        else:
            print('aaaaaaaaa')
            cart_item.delete()
    except:
        pass
    return redirect('cart')



def cart(request, total=0, cart_items=0):
   
    
        
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items= CartItem.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            total += cart_item.product.price
        tax = (5 * total)/100
        grand_total = tax+total
        print(tax,grand_total)
    except:
        pass
        
    context = {
            'total': total,
            'cart_items': cart_items,
            'tax': tax,
            'grand_total': grand_total,
            
        }

    return render(request, 'cart/cart.html', context)


def contact(request):
    return render(request,'cart/contact.html')


@login_required(login_url='login')
    
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items= CartItem.objects.filter(user=request.user)
        else:
                
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
                
            total += cart_item.product.price 
                
            tax = (5 * total)/100
            grand_total = tax+total
    except:
            pass
    context = {
            'total': total,
            'cart_items': cart_items,
            'tax': tax,
            'grand_total': grand_total,
        }
  
    return render(request, 'cart/checkout.html', context)

def billing(request):
    details = Accounts.objects.all()

    userdetails = Accounts(request.POST,request.FILES,instance=details)
    userdetails.save()
    context={
        'details':details,
        'userdetails':userdetails,
    }
    return render(request,'cart/checkout.html',context)