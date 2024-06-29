from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from goods.models import Products


# Create your views here.

def catalog(request, category_slug):
    if category_slug == 'all':
        goods = Products.objects.all()
    else:
        goods = get_object_or_404(Products.objects.filter(category__slug=category_slug))
    context = {
        'title': 'Home - Каталог',
        'goods': goods
    }

    return render(request, 'goods/catalog.html', context)


def product(request, product_slug):
    try:
        product = Products.objects.get(slug=product_slug)
    except Products.DoesNotExist:
        # Обработка ситуации, когда продукт не найден
        return HttpResponse("Продукт не найден", status=404)

    context = {
        'product': product
    }
    return render(request, 'goods/product.html', context=context)
