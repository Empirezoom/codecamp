from django.db import models
from django.contrib.auth.models import User
from home.models import Phone

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    pix = models.ImageField(upload_to='customer')

    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'customer'
        managed = True
        verbose_name = 'Customer'
        verbose_name_plural = 'Customer'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    price = models.IntegerField()
    qty = models.IntegerField()
    amount = models.CharField(max_length=50)
    paid = models.BooleanField()

    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'cart'
        managed = True
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    amount = models.IntegerField()
    paid = models.BooleanField()
    phone = models.CharField(max_length=50)
    order_no = models.CharField(max_length=50)
    pay_code = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username 
    
    class Meta:
        db_table = 'payment'
        managed = True
        verbose_name = 'Payment'
        verbose_name_plural = 'Payment'