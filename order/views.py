
from itertools import product
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.views import order_complete

from cart.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct
import datetime
from .models import Order
from django.views.decorators.csrf import csrf_exempt
from cart.views import *
import json
from stocks.models import products
from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os


def placeorder(request, total=0, quantity=0):

    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('stocks')
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        quantity += cart_item.quantity
        total += cart_item.product.price

    tax = (5 * total)/100
    grand_total = total + tax
    if request.method == 'POST':
        print('main if')
        form = OrderForm(request.POST)

        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.tax = tax
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            client = razorpay.Client(
                auth=('rzp_test_D2kTxkbeGLQVTC', 'rPgNRKnER3ezKyobOVLj8zH9'))

            DATA = {
                "amount": int(data.order_total) * 100,
                "currency": "INR",
                "payment_capture": 1,
            }
            payment = client.order.create(data=DATA)
            print(payment)

        order = Order.objects.get(
            user=current_user, is_ordered=False, order_number=order_number)
        context = {
            'order': order,
            'cart_items': cart_items,
            'tax':tax,
            'total': total,
            'grand_total': grand_total,
            'payment': payment,
        }
        return render(request, 'order/payment.html', context)
    else:
        return redirect('checkout')


def pdf(request):
    
    ordered_products = OrderProduct.objects.filter(user=request.user)
    
    context = {
        'ordered_products':ordered_products,
    }   
    return render(request,'order/pdfbase.html',context)

def pdf_report(request):
    ordered_products = OrderProduct.objects.filter(user=request.user,)
    template_path = 'accounts/pdfreport.html'
    context = {'ordered_products':ordered_products}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="planreport.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status=pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('we had some errors <pre>'+ html + '</pre>')
    return response
    