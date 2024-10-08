from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Products
from goods.utils import q_search


# Create your views here.

def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale')
    order_by = request.GET.get('order_by')
    query = request.GET.get('q', None)
    lower_price_range = request.GET.get('lower_price_range')
    upper_price_range = request.GET.get('upper_price_range')

    if category_slug == 'all':
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = Products.objects.filter(category__slug=category_slug)

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != 'default':
        if order_by == 'price':
            goods = goods.order_by(order_by)
        elif order_by == '-price':
            goods = goods.order_by(order_by)

    if lower_price_range and upper_price_range:
        goods = goods.filter(price__range=(lower_price_range, upper_price_range))

        if not goods.exists():
            paginator = Paginator(goods, 3)
            current_page = paginator.get_page(page)
            context = {
                'title': 'Home - Каталог',
                'goods': current_page,
                'slug_url': category_slug,
                'no_results': True
            }

            return render(request, 'goods/catalog.html', context)

    paginator = Paginator(goods, 3)
    current_page = paginator.get_page(page)

    context = {
        'title': 'Home - Каталог',
        'goods': current_page,
        'slug_url': category_slug,
        'no_results': False
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
