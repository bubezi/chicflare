from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from .models import *
from .filters import ProductFilter
from django.db.models import query
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.crypto import get_random_string


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        context = {'customer': customer}
    else:
        context = {}
    return render(request, 'store/home.html', context)


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()

    myFilter = ProductFilter(request.GET, queryset=products)
    products = myFilter.qs

    if request.user.is_authenticated:
        customer = request.user.customer
        context = {'customer': customer, 'products': products, 'cartItems': cartItems, 'myFilter': myFilter}
        return render(request, 'store/store.html', context)
    else:
        return redirect('login')



def payment(request):
    context = {}
    if request.user.is_authenticated:
        customer = request.user.customer
        context = {'customer': customer}
        return render(request, 'store/payment.html', context)
    else:
        return redirect('login')


# def details(request):
#     products = Product.objects.all()
#
#     myFilter = ProductFilter(request.GET, queryset=products)
#     products = myFilter.qs
#
#     if request.user.is_authenticated:
#         context = {'products': products,
#                    'myFilter': myFilter}
#         return render(request, 'store/details.html', context)
#     else:
#         return HttpResponseBadRequest('Invalid Request')


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    if request.user.is_authenticated:
        return render(request, 'store/cart.html', context)
    else:
        return redirect('login')


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    if request.user.is_authenticated:
        return render(request, 'store/checkout.html', context)
    else:
        return redirect('login')


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

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

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)


# def search(request):
#     if request.method == "POST":
#         searched = request.POST.get('searched')
#         search_items = Product.objects.filter(Q(name__contains=searched)
#                                               | Q(fuel_type=searched)
#                                               | Q(model=searched)
#                                               | Q(transmission=searched)
#                                               | Q(details=searched)
#                                               | Q(price=searched))
#
#         context = {'searched': searched,
#                    'search_items': search_items}
#     else:
#         context = {}
#
#     return render(request, 'store/results.html', context)


# def contact(request):
#     context = {}
#     return render(request, 'store/contact.html', context)


def view_product(request, pk):
    product = Product.objects.get(name=pk)

    if request.user.is_authenticated:
        context = {'product': product}
        return render(request, 'store/view_product.html', context)
    else:
        return redirect('login')
