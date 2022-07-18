from django.db import models
from accounts.models import Accounts
from stocks.models import products

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Accounts,on_delete = models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method  = models.CharField(max_length=100)
    amount_paid =models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return self.payment_id  
    
class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )
    
    user = models.ForeignKey(Accounts,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete =models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=20)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone =models.CharField(max_length=20)
    email = models.EmailField(max_length=50) 
    address_line1 =models.CharField(max_length=50)
    address_line2 =models.CharField(max_length=50,blank=True) 
    country =models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    order_note =models.CharField(max_length=50,blank=True) 
    order_total = models.FloatField(max_length=100,blank=True)
    tax = models.FloatField()
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
  
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
  
    def full_address(self):
            return f'{self.address_line1} {self.address_line2}'
    def __str__(self):
        return self.first_name 
    
class OrderProduct(models.Model):
     order = models.ForeignKey(Order,on_delete=models.CASCADE)
     payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
     user = models.ForeignKey(Accounts,on_delete=models.CASCADE)
     product = models.ForeignKey(products,on_delete=models.CASCADE)
     quantity = models.IntegerField()
     product_price =models.FloatField()
     ordered = models.BooleanField(default=False)
     created_at = models.DateTimeField(auto_now_add =True)
     updated_at=models.DateTimeField(auto_now = True)
     
     def __str__(self):
         return self.product.product_name  
     
class productpayment(models.Model):
    name=models.CharField(max_length=100,blank=True)
    amount=models.CharField(max_length=100,blank=True)
    email=models.CharField(max_length=200)
    order_id =models.CharField(max_length=1000)
    paid=models.BooleanField(default=False)
    razorpay_payment_id=models.CharField(max_length=100,blank=True)
    