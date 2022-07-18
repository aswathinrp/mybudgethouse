from django.urls import path
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.stocks,name='stocks'),
    path('category/<slug:category_slug>/',views.stocks,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('wishlist_add/<int:id>/',views.wishlist_add,name='wishlist_add'),
    path('wishlist_remove/<int:id>/',views.wishlist_remove,name='wishlist_remove'),
]
