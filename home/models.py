from django.db import models

# Create your models here.

class CompanyProfile(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logo')
    carousel1 = models.ImageField(upload_to='carousel')
    carousel2 = models.ImageField(upload_to='carousel')
    carousel3 = models.ImageField(upload_to='carousel')
    banner = models.ImageField(upload_to='banner')
    favicon = models.ImageField(upload_to='favicon')
    about = models.TextField()
    copyright = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'companyprofile'
        managed = True
        verbose_name = 'CompanyProfile'
        verbose_name_plural = 'CompanyProfile'
    

class Type(models.Model):
    brand = models.CharField(max_length=50)
    color = models.CharField(max_length=50, blank=True, null=True)
    

    def __str__(self):
        return self.brand

    class Meta:
        db_table = 'type'
        managed = True
        verbose_name = 'Type'
        verbose_name_plural = 'Type'
    

class Phone(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    pix = models.ImageField(upload_to='pix')
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    network = models.CharField(max_length=50)
    launch = models.CharField(max_length=50)
    memory = models.CharField(max_length=50)
    camera = models.CharField(max_length=50)
    featured = models.BooleanField()
    best_selling = models.BooleanField()
    latest = models.BooleanField()
    uploaded_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'phone'
        managed = True
        verbose_name = 'Phone'
        verbose_name_plural = 'Phone'

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField()
    sent = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
    
    class Meta:
        db_table = 'contact'
        managed = True
        verbose_name = 'Contact'
        verbose_name_plural = 'Contact'