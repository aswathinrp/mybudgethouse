from django.contrib import admin
import admin_thumbnails 
from stocks.views import wishlist

from . models import ProductGallery, products,Wishlist
from . models import ProductGallery

# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra=1




class productadmin(admin.ModelAdmin):
    list_display = ('product_name','price','category','created_date','max_area','bedrooms','bathrooms','floors','parking')
    prepopulated_fields = {'slug':('product_name',)}
    inlines =[ProductGalleryInline]
admin.site.register(products, productadmin)
admin.site.register(Wishlist)
admin.site.register(ProductGallery)