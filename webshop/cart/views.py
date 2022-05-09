from django.shortcuts import render, get_object_or_404

from django.http import JsonResponse

from products.models import Product
from .basket import Basket

import json

# Create your views here.

def display_cart(request):
    context = {
        'cart' : Basket(request).__iter__(),
        'quantity' : Basket(request).__len__(),
        'sub_total' : Basket(request).get_total_price(),
    }
    
    return render(request, 'cart/cart.html', context)

def add_to_cart(request):
    basket = Basket(request)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            productId = data.get('productId')
            product = get_object_or_404(Product, id=productId)
            basket.add(product=product)
            quantity = basket.__len__()
            response = JsonResponse({'quantity': quantity})
            return response


def delete_from_cart(request):
    basket = Basket(request)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'DELETE':
            data = json.load(request)
            productId = data.get('productId')

            data = basket.delete(product=productId)

            response = JsonResponse(data)
            return response