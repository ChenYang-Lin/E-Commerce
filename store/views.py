from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import datetime

from .models import *
from .forms import EditProfileForm, AddProductForm
from . utils import cookieCart, cartData, guestOrder

# Create your views here.
def index(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}

    return render(request, 'store/index.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']
    print(order)

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    order = data['order']

    customer = {}
    if request.user.is_authenticated:
        customer = request.user.customer
        
    context = {'items':items, 'order':order, 'cartItems': cartItems, 'customer':customer}
    return render(request, 'store/checkout.html', context)

@login_required(login_url='login')
def history(request):
    customer = request.user.customer

    # items in cart
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items

    # list of purchased orders
    orders = Order.objects.filter(customer=customer, complete=True)
    orderList = []
    for order in orders:
        object = {
            'order': order,
            'items': order.orderitem_set.all(),
        }
        orderList.append(object)

    context = {'orderList':orderList, 'cartItems': cartItems}

    return render(request, 'store/history.html', context)

@login_required(login_url='login')
def profile(request):
    customer = request.user.customer

    # items in cart
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items

    context = { 'customer':customer, 'cartItems': cartItems }
    return render(request, 'store/profile.html', context)

@login_required(login_url='login')
def editProfile(request):
    customer = request.user.customer

    # items in cart
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
 
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = EditProfileForm(instance=customer)

    context = { 'customer':customer, 'cartItems': cartItems, 'form': form }
    return render(request, 'store/edit-profile.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', cookieCart, productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    data = cartData(request)
    cartItems = data['cartItems']

    return JsonResponse(cartItems, safe=False)

def processOrder(request):
    # print("data: ", request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)
    
    # Both authenticated user or guest user
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total: # make sure total is correct. frontend paypal total matches with backend order toal
        order.complete = True
    order.save()

    
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse("Payment complete!", safe=False)

@login_required(login_url='login')
def addProduct(request):
    # if not admin/superuser, redirect to home page
    if not request.user.is_superuser:
        return redirect('/')

    # items in cart
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items

    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form = AddProductForm()

    context = { 'cartItems': cartItems, 'form': form }
    return render(request, 'store/add-product.html', context)