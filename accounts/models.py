from distutils.command.upload import upload
from email.policy import default

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('user must have an email address')
        if not username:
            raise ValueError('user must have an email address')
        
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
                       
            
        )
        
        user.set_password(password)
        user.save(using = self._db)
        return user
        
    def create_superuser(self,first_name,last_name,email,username,password):
        user=self.create_user(
            email = self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
    
class Accounts(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=50,unique=True)
   
    
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    objects=MyAccountManager()
    
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,add_label):
        return True
    
class UserProfile(models.Model):
    user = models.OneToOneField(Accounts,on_delete=models.CASCADE)
    phone_number=models.IntegerField(blank=True,null=True)
    profile_pic =models.ImageField(blank=True,upload_to ='userprofile')
    city = models.CharField(max_length=20,blank =True,null=True)
    state = models.CharField(max_length=20,blank = True,null=True)
    
    def __str__(self):
        return self.user.first_name