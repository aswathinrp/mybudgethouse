from accounts.models import Accounts
from category.models import category
from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.
class products(models.Model):
    product_name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(max_length=255,unique=True)
    description = models.TextField(max_length=555,blank=True)
    max_area = models.IntegerField(null=True,blank=True)
    bedrooms = models.IntegerField(null=True,blank=True)
    bathrooms = models.IntegerField(null=True,blank=True)
    floors = models.IntegerField(null=True,blank=True)
    parking = models.TextField(max_length=100, null=True)
    price = models.IntegerField()
    quantity = models.IntegerField(null=True)
    images = models.ImageField(upload_to = 'photos/products')
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add= True)
    # users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="user_wishlist",blank=)
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
    def __str__(self):
        return self.product_name
    
class Wishlist(models.Model):
    user = models.ForeignKey(Accounts,on_delete=models.CASCADE)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.product_name
    
    
class ProductGallery(models.Model):
    product = models.ForeignKey(products,default=None,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products',max_length=255)
    
    def __str__(self):
        return self.product.product_name
    class Meta:
        verbose_name='productgallery'
        verbose_name_plural='product gallery'
        