
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from accounts.models import MyAccountManager

from stocks.models import products
from accounts.models import Accounts
from category.models import category
from django.template.defaultfilters import slugify
from . forms import add_product
from . forms import edit_product
from order.models import Order, OrderProduct
from order.models import Payment
from django.db.models import Q
# Create your views here.

# account = Accounts.objects.all()


def adminlogin(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None and user.is_admin:
            auth.login(request, user)
            return redirect(home)
        else:
            messages.error(request, 'invalid entry !')
            return redirect(adminlogin)

    else:
        return render(request, 'administrator/adminlogin.html')


def logout(request):
    if 'email' in request.session:
        request.session.flush()   # clear
    return redirect(adminlogin)


def home(request):

    return render(request, 'administrator/home.html')


def dashboard(request):
    search_key = request.GET.get('key') if request.GET.get('key') != None else ''
    # if 'username' in request.session:
    user_list = Accounts.objects.filter(username__istartswith = search_key)
    return render(request, 'administrator/dashboard.html', {'Accounts': user_list})

    # else:

    #     account = Accounts.objects.all()
    #     context = {'Accounts': account}
        
    # return render(request, 'dashboard.html', context)
    
# return redirect(dashboard)


def clients(request):
    account = Accounts.objects.all()
    context = {'Accounts': account}

    return render(request, 'administrator/clients.html', context)


def stock_table(request):
    search_key = request.GET.get('key') if request.GET.get('key') != None else ''
    # if 'product_list' in request.session:
    product_list = products.objects.filter(product_name__istartswith = search_key)
    return render(request, 'administrator/stock_table.html', {'products': product_list})
    

   


def add(request):
    if request.method == 'POST':
        form = add_product(request.POST, request.FILES)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            form.save()
            slug = slugify(product_name)
            print(product_name)
            product = products.objects.get(product_name=product_name)
            product.slug = slug
            product.save()
            print("product created")

    form = add_product()
    product = products.objects.all()
    context = {
        'product': product,
        'form': form
    }
    return render(request, 'administrator/add.html', context)


def delete(request, id):
    product = products.objects.get(id=id)
    product.delete()
    return redirect(stock_table)


def edit(request, id):
    product = products.objects.get(id=id)

    if request.method == 'POST':
        form = edit_product(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            slug = slugify(product_name)
            product = form.save()
            product.product_slug = slug
            form.save()
            return redirect('stock_table')
    else:
        form =  edit_product(instance=product)
    context = {
        'form' : form,
        'product':product,
    }
    return render (request,'administrator/edit.html',context)
    


def orderdetail(request,order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
   
    order=Order.objects.get(order_number=order_id)
    
    # product_id =request.GET.get('product_id')
    subtotal=0
    for i in order_detail:
        subtotal+=i.product_price * i.quantity
    context ={
        'order':order,
        'order_detail':order_detail,
        'subtotal':subtotal,
        
    }
    
    return render(request,'administrator/orderdetail.html',context)

def block_user(request,id):
    account = Accounts.objects.get(id=id)
    if account.is_active:
        account.is_active= False
        account.save()
    else:
        account.is_active= True
        account.save()
    return redirect('dashboard')    
    
def back(request):
    return render(request,'administrator/stock_table.html')

def paymenthistory(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            paid =Payment.objects.order_by('payment_id').filter(Q(payment_id__icontains=keyword))
        if not paid.exists():
            messages.error(request,'no match found')
            return redirect(request,'administrator/paymenthistory.html')
    else:
        paid = Payment.objects.all().order_by('payment_id')
    context ={
        'paid':paid,
    }

    return render(request,'administrator/paymenthistory.html',context)
def categorylist(request):
    categories = category.objects.all()
    product = products.objects.all()
    context = {
        'categories':categories,
        'product':product,
    }
    return render(request,'administrator/categorylist.html',context)



def orderhistory(request):
    orders = Order.objects.all()
    # user=request.user,order_number=).order_by('-created_at')
   
    
    product_id =request.GET.get('product_id')
    context ={
        'orders':orders,
        'product_id':product_id,
    }
    
    return render(request,'administrator/orderhistory.html',context)