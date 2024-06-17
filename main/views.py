from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories


def index(request) -> HttpResponse:

    categories = Categories.objects.all()

    context = {
        'title': 'Home - Главная',
        'content': 'Perfume&Symphonies',
        'categories': categories,
    }

    return render(request, 'main/index.html', context)


def about(request) -> HttpResponse:
    context = {
        'title': 'Home - О нас',
        'content': 'О нас',
        'text_on_page': 'Текст о том какой классный магазин'
    }

    return render(request, 'main/about.html', context)

