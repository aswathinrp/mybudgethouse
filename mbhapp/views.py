
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from razorpay import Order
from stocks.models import products
from order.models import Order
# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST[username]
        password = request.POST[password]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            request.session['username'] = username
            return redirect(index)
        else:
            messages.error(request, 'invalid entry !')
            return redirect(login)
    else:
        return render(request, 'accounts/login.html')


def index(request):
    product = products.objects.all()
    context = {'products': product}


    # if 'username' in request.session:
    return render(request,'index.html',context)
    # else:
    #     return redirect('login')

def logout(request):
    if 'username' in request.session:
        request.session.flush()   # clear
    return redirect('/')

def contact(request):
    return render(request,'cart/contact.html')

def userdashboard(request):
    orders = Order.objects.order_by('created_at').filter(user =request.user)
    orders_count=orders.count()
    
    context={
        'orders_count': orders_count,
    }
    return render(request,'mbhapp/userdashboard.html',context)

def about(request):
    return render(request,'accounts/about.html')