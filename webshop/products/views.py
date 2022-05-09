from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.views import generic

from .models import Product
from .forms import ProductModelForm

#imports for ajax and json
import json

# Create your views here.

class ProductListView(generic.ListView):
    model = Product
    queryset = Product.objects.all()

    def get_queryset(self):
        if self.request.method == 'GET' and 'q' in self.request.GET:
            query = self.request.GET.get('q')
            result = Product.objects.filter(name__icontains=query).order_by('name', 'price')
            if result:
                return result
            else:
                return Product.objects.filter(code__icontains=query).order_by('name', 'price')

        else:
            return Product.objects.all()


class ProductDetailView(generic.DetailView):
    model = Product

class ProductCreateView(generic.CreateView):
    template_name = 'products/product_create.html'
    form_class = ProductModelForm
    queryset = Product.objects.all()
    success_url = '/'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('products'))


'''
def Cart(request):
    # request.is_ajax() is deprecated since django 3.1
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            productId = data.get('productId')
            product = Product.objects.get(id=productId)
            data = {
                'id': productId,
                'name': product.name,
                'code': product.code,
                'price': product.price,
                'description': product.description
            }
            return JsonResponse(data)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

'''