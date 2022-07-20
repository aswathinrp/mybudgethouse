from django.urls import path
from . import views 

urlpatterns = [
   path('placeorder/',views.placeorder,name="placeorder"),
   path('pdf/<int:order_id>',views.pdf,name='pdf'),
   path('pdf_report/<int:order_id>',views.pdf_report,name='pdf_report')
]