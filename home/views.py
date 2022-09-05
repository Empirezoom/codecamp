import requests
import uuid
import json 

from django.shortcuts import redirect, render
from django.http import HttpResponse 
from django.core.paginator import Paginator
from django.contrib import messages 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils.html import format_html
from . models import CompanyProfile, Phone, Type
from .forms import ContactForm
from userprofile.models import Customer
from userprofile.forms import *

# Create your views here.

def home(request):
    featured = Phone.objects.filter(featured=True)
    bestselling = Phone.objects.filter(best_selling=True)
    latest = Phone.objects.filter(latest=True)

    context = {
        'featured': featured,
        'bestselling': bestselling,
        'latest': latest,
    }

    return render(request, 'index.html', context)

def products(request):
    product = Phone.objects.all()
    p = Paginator(product, 8)
    page = request.GET.get('page')
    paginate = p.get_page(page)

    context = {
        'paginate': paginate,
    }

    return render(request, 'products.html', context)

def category(request, id):
    brand = Type.objects.get(pk=id)
    phonecat = Phone.objects.filter(type_id = id)

    context = {
        'brand': brand,
        'phonecat': phonecat,
    }

    return render(request, 'category.html', context)

def detail(request, id, slug):
    phonedet = Phone.objects.get(pk=id)

    context = {
        'phonedet': phonedet,
    }

    return render(request, 'detail.html', context)

def about(request):
    aboutus = CompanyProfile.objects.get(pk=1)

    context = {
        'aboutus': aboutus
    }

    return render(request, 'about.html', context)

def contact(request):
    contact = ContactForm()
    if request.method == 'POST':
        contact = ContactForm(request.POST)
        if contact.is_valid():
            contact.save()
            messages.success(request,'Your message has been sent successfully, one of our representative will get back to you shortly!!')
            return redirect('home')

    context = {
        'contact': contact 
    }

    return render(request,'contact.html', context)

# authentication
def signout(request):
    logout(request)
    messages.success(request,'You are now signed out')
    return redirect('home')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'login successful!!')
            return redirect('home')
        else:
            messages.info(request, 'Username/Password is incorrect')

    return render(request, 'signin.html')

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        phone = request.POST['phone']
        address = request.POST['address']
        pix = request.POST['pix']
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            newuser = Customer(user=user)
            newuser.username = user.username
            newuser.first_name = user.first_name
            newuser.last_name = user.last_name
            newuser.email = user.email
            newuser.phone = phone 
            newuser.address = address 
            newuser.pix = pix 
            newuser.save()
            messages.success(request, f'Congratulations {user.username} your registration is successful')
            return redirect('signin')
        else:
            messages.error(request, form.errors)

    return render(request, 'signup.html')

# authentication done

# userprofile
@login_required(login_url='signin')
def profile(request):
    userprof = Customer.objects.get(user__username = request.user.username)

    context = {
        'userprof':userprof
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def profile_update(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    form = ProfileForm(instance=request.user.customer)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.customer)
        if form.is_valid():
            user = form.save()
            new = user.first_name.title()
            messages.success(request, f'Dear {new}, your profile has been updated successfully')
            return redirect('profile')
        else:
            new = user.first_name.title()
            messages.error(request, f'Dear {new}, your profile update generated the following errors: {form.errors}')
            return redirect('profile_update')

    context = {
        'userprof':userprof
    }

    return render(request, 'profile_update.html', context)

@login_required(login_url='signin')
def password_update(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        new = request.user.username.title()
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Dear {new} your password change is successful!!!')
            return redirect('profile')
        else:
            messages.error(request, f'Dear {new} your password change is not successful, {form.errors}')
            return redirect('password_update')

    context = {
        'userprof':userprof,
        'form':form
    }

    return render(request, 'password_update.html', context)

# userprofile done

#cart
@login_required(login_url='signin')
def add_to_cart(request):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        devphone = request.POST['phoneid']
        main = Phone.objects.get(pk=devphone)
        cart = Cart.objects.filter(user__username = request.user.username, paid=False)
        if cart:
            basket = Cart.objects.filter(user__username = request.user.username, paid=False, phone=main.id, qty=quantity).first()
            if basket:
                basket.qty += quantity
                basket.amount = main.price * basket.qty 
                basket.save()
                messages.success(request, format_html('one item added to cart ... <a href="http://3.80.62.88/cart">view cart</a>'))
                return redirect('home')
            else:
                newitem = Cart()
                newitem.user = request.user 
                newitem.phone = main 
                newitem.price = main.price
                newitem.qty = quantity 
                newitem.amount = main.price * quantity 
                newitem.paid = False 
                newitem.save()
                messages.success(request, format_html('one item added to cart ... <a href="http://3.80.62.88/cart">view cart</a>'))
                return redirect('home')
        else:
            newcart = Cart()
            newcart.user = request.user 
            newcart.phone = main 
            newcart.price = main.price
            newcart.qty = quantity 
            newcart.amount = main.price * quantity 
            newcart.paid = False 
            newcart.save()
            messages.success(request, format_html('one item added to cart ... <a href="http://3.80.62.88/cart">view cart</a>'))
            return redirect('home')

@login_required(login_url='signin')
def cart(request):
    cart = Cart.objects.filter(user__username = request.user.username, paid=False)
    for item in cart:
        item.amount = item.price * item.qty 
        item.save()

    subtotal = 0 
    vat = 0 
    total = 0 

    for item in cart: 
        subtotal += item.amount 

    vat = 0.075 * subtotal 
    total = subtotal + vat 

    context = {
        'cart':cart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total 
    }

    return render(request, 'cart.html', context)

def increase(request):
    if request.method == 'POST':
        qty_item = request.POST['quant_id']
        new_qty = request.POST['quant']
        newqty = Cart.objects.get(pk=qty_item)
        newqty.qty = new_qty 
        newqty.amount = newqty.price * newqty.qty 
        newqty.save()
        messages.success(request, 'Quantity updated')
        return redirect('cart')

def delete(request):
    if request.method == 'POST':
        del_item = request.POST['del_id']
        Cart.objects.filter(pk=del_item).delete()
        messages.success(request, 'one item deleted')
        return redirect('cart')
#cart done

@login_required(login_url='signin')
def checkout(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    cart = Cart.objects.filter(user__username = request.user.username, paid=False)
    for item in cart:
        item.amount = item.price * item.qty 
        item.save()

    subtotal = 0 
    vat = 0 
    total = 0 

    for item in cart: 
        subtotal += item.amount 

    vat = 0.075 * subtotal 
    total = subtotal + vat 

    context = {
        'cart':cart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
        'userprof':userprof,
    }

    return render(request, 'checkout.html', context)

@login_required(login_url='signin')
def pay(request):
    if request.method == 'POST':
        api_key = 'sk_test_628e6e1f0bbc950dbb7dcd15ff6aa4da2e434e65' #secret key from paystack
        curl = 'https://api.paystack.co/transaction/initialize' #paystack call url 
        cburl = 'http://3.80.62.88/callback' #payment thank you page 
        ref = str(uuid.uuid4()) #reference number required by paystack as additional order number 
        profile = Customer.objects.get(user__username = request.user.username)
        order_no = profile.id 
        total = float(request.POST['total']) * 100 #total amount to be charged from the user card
        user = User.objects.get(username = request.user.username) #query the user model for user details 
        email = user.email #store user email to send to paystack 
        first_name = request.POST['first_name'] #collect from the template incase there is a change
        last_name = request.POST['last_name'] #collect from the template incase there is a change
        phone = request.POST['phone'] #collect from the template incase there is a change

        #collect data to send to paystack via call
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference': ref, 'amount': int(total), 'email': user.email, 'callback_url': cburl, 'order_number': order_no, 'currency': 'NGN'}

        #make a call to paystack
        try:
            r = requests.post(curl, headers=headers, json=data) #pip install requests at this point 
        except Exception:
            messages.error(request, 'Network busy, try again')
        else:
            transback = json.loads(r.text)
            rdurl = transback['data']['authorization_url']

            account = Payment()
            account.user = user 
            account.first_name = user.first_name
            account.last_name = user.last_name
            account.amount = total/100 
            account.paid = True 
            account.phone = phone 
            account.pay_code = ref 
            account.order_no = order_no 
            account.save()

            return redirect(rdurl)

    return redirect('checkout')

@login_required(login_url='signin')
def callback(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    cart = Cart.objects.filter(user__username = request.user.username, paid=False)

    for item in cart: 
        item.paid = True 
        item.save()

        phone = Phone.objects.get(pk=item.phone.id)
        phone.save()

    context = {
        'userprof':userprof,
        'cart':cart,
        'phone':phone
    }

    return render(request, 'callback.html', context)