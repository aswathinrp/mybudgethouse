from django.urls import path
from . import views 

urlpatterns = [
   path('placeorder/',views.placeorder,name="placeorder"),
   path('pdf/',views.pdf,name='pdf'),
   path('pdf_report/',views.pdf_report,name='pdf_report')
]