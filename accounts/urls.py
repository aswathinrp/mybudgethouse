
from django.urls import path
from . import views


urlpatterns = [
  
  path('login/',views.login,name='login'),
  path('register/',views.signin,name='register'),
  path('logout/',views.logout,name='logout'),
  path('activate/<uidb64>/<token>/',views.activate,name='activate'),
  path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
  path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
  path('resetpassword/',views.resetpassword,name='resetpassword'),
  path('myorders/',views.myorders,name='myorders'),
  path('edit_profile/',views.edit_profile,name='edit_profile') ,
  path('change_password/',views.change_password,name='change_password') ,
  path('userdashboard/',views.userdashboard,name='userdashboard'),
  path('payment',views.payment,name='payment'),
  path('order_complete',views.order_complete,name='order_complete'),
  path('successs',views.successs,name='successs'),
 
]