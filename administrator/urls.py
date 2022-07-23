from django.urls import path
from . import views


urlpatterns = [
               
                path('logout/',views.logout,name='logout_admin'),
                path('add/',views.add,name="add"),
                path('delete/<int:id>',views.delete,name="delete"),
                path('edit/<int:id>',views.edit,name='edit'),
               
                path('adminlogin/',views.adminlogin,name='adminlogin'),
                # path('home/',views.home,name='home'),
                # path('dashboard/',views.dashboard,name='dashboard'),
                path('clients/',views.clients,name='clients'),
                path('table/',views.stock_table,name='stock_table'),
                path('orderdetail/<int:order_id>',views.orderdetail,name='orderdetail'),
                path('categorylist/',views.categorylist,name='categorylist'),
                path('orderhistory/',views.orderhistory,name='orderhistory'),
                path('block_user/<int:id>',views.block_user,name='block_user'),
                path('paymenthistory',views.paymenthistory,name='paymenthistory'),
                path('AdminHome',views.AdminHome,name='AdminHome'),
                path('back',views.back,name='back'),
               
              ]