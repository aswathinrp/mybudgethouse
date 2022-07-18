
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('contact/',views.contact,name='contact'),
    
    path('about/',views.about,name='about'),

   
]