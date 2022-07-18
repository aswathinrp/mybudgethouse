
from django.conf import settings
from django.contrib import admin
from django.urls import path,include

from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _


urlpatterns = [
   
    path('securelogin/', admin.site.urls),
    path('',include('mbhapp.urls')),
    path('accounts/', include('accounts.urls')),
    path('stocks/',include('stocks.urls')),
    path('cart/',include('cart.urls')),
    path('order/',include('order.urls')),
    path('administrator/',include('administrator.urls')),
    ]
urlpatterns=urlpatterns+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

