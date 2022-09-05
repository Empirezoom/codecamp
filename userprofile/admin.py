from django.contrib import admin
from .models import *

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'phone', 'email', 'pix']

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'price', 'qty', 'amount', 'paid']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone', 'amount', 'pay_code', 'paid', 'payment_date']

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Payment,PaymentAdmin)