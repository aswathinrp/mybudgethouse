from django.db import models
from stocks . models import products
from accounts.models import Accounts
# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user=models.ForeignKey(Accounts,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField(null=True)

    def subtotal(self):
        return (self.product.price * self.product.quantity)
    def __str__(self):
        return self.product.product_name
    
class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email