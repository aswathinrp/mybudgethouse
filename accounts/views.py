
from itertools import product
from django.views import View
import razorpay
import email
from stocks.models import ProductGallery, products  
from order.models import Payment
from email import message
from re import U
from order.models import OrderProduct, productpayment
import razorpay
from tabnanny import check
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages, auth
from accounts.models import Accounts
from mbhapp.views import index
from .models import Accounts, UserProfile
from .forms import RegistrationForm,UserForm,UserProfileForm
from django.contrib.auth.decorators import login_required
from cart.views import _cart_id
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from cart . models import Cart, CartItem
from order.models import Order,OrderProduct
import json
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

from category.models import category
# Create your views here.

def signin(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Accounts.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, password=password, username=username)

            user.save()

            current_site = get_current_site(request)
            mail_subject = 'please activate your account'
            message = render_to_string('email_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),


            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Registration successfull')
            return redirect('register')
    else:

        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(
                    cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # for item in cart_item:
                    #     item.user = user
                    #     item.save()
            except:
                pass
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request,'accounts/login.html')


@login_required(login_url='login')
def logout(request):

    auth.logout(request)
    messages.success(request, 'you are logged out')
    return redirect('index')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = Accounts._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Accounts.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for registering with us ')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Accounts.objects.filter(email=email).exists():
            user = Accounts.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = 'please reset  your password'
            message = render_to_string('resetpassword_email_verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),


            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, 'password reset email has been sent to your account')
            return redirect('login')
        else:
            messages.error(request, 'account does not exist')
            return redirect('forgotpassword')
    return render(request, 'accounts/forgotpassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Accounts._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Accounts.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'this link hasbeen expired')
        return redirect('login')


def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Accounts.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'password reset successfull')
            return redirect('login')
        else:
            messages.error(request, 'password do not match')
            return redirect('resetpassword')
    else:
        return render(request, 'accounts/resetpassword.html')
    
@login_required(login_url='login')    
def myorders(request):
    orders =Order.objects.filter(user=request.user).order_by('-created_at')
    context ={
        'orders':orders
    }
    return render(request,'accounts/myorders.html',context)

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile,user = request.user)
    if request.method=='POST':
        user_form =UserForm(request.POST,instance=request.user)
        profile_form = UserProfileForm(request.POST,request.FILES,instance = userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save();
            profile_form.save();
            messages.success(request,'your profile is updated')
            return redirect('edit_profile')
    else:
        user_form =UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
                'user_form' :user_form,
                'profile_form' : profile_form,
                'userprofile': userprofile,
            }
            
            
    return render(request,'accounts/edit_profile.html',context)

@login_required(login_url='/login/')
def change_password(request):
    if request.method=='POST':
        current_password= request.POST['current_password']
        new_password= request.POST['new_password']
        confirm_password= request.POST['confirm_password']
        
        user = Accounts.objects.get(username__exact=request.user.username)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'password updated successfully')
                return redirect('change_password')
            else:
                messages.error(request,'please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request,'password does not match')
            return redirect('change_password')
    return render(request,'accounts/change_password.html')

def payment(request):
    body=json.loads(request.body)
    order = Order.objects.get(user=request.user,is_ordered =False, order_number = body['order_id'])
    
    payment = Payment(
        user=request.user,
        payment_id=body['razorpay_payment_id'],
        payment_method =body['payment_method'],
        amount_paid = body['amount_paid'],
        status= body['status'],
    ) 
    payment.save()
    order.payment=payment
    order.is_ordered= True
    order.save()
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
        
    cart_items = CartItem.objects.filter(user=request.user).delete()
        
    mail_subject = 'Thank you for your order! Visit Again'
    message = render_to_string('order_received_email.html', {
        'user': request.user,
        'order':order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    
    
    data = {
        'order_number':order.order_number,   
        'transID': payment.payment_id,
    }
    return JsonResponse(data)



def successs(request):
    
    return render(request,'success.html')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number = order_number,is_ordered =True)
        ordered_products =OrderProduct.objects.filter(order_id = order.id)
        template_path = 'accounts/pdfreport.html'
        context = {'ordered_products':ordered_products,
                   }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="planreport.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status=pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('we had some errors <pre>'+ html + '</pre>')
        
        subtotal=0
        for i in ordered_products:
            subtotal += i.product_price
            
        payment = Payment.objects.get(payment_id=transID)
        context = {
            'order': order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID':payment.payment_id,
            'payment':payment,
            'subtotal':subtotal,
        }
        return render(request,'accounts/order_complete.html',context)
    except (Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('index')
    
    
    # return render(request,'order_complete.html')

def about(request):
    return render(request,'accounts/about.html')

def userdashboard(request):
    userprofile = UserProfile.objects.get_or_create(user=request.user)
    orders = Order.objects.order_by('created_at').filter(user=request.user)
    orders_count=orders.count()
    
    context={
        'orders_count': orders_count,
    }
    return render(request,'accounts/userdashboard.html',context)
