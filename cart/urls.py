from django.urls import path
from . import views
urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<int:products_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:products_id>/<int:cart_item_id>',views.remove_cart,name='remove_cart'),
    path('contact',views.contact,name='contact'),
    path('checkout/',views.checkout,name='checkout'),
    ]   