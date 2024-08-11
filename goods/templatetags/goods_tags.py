from django import template
from urllib.parse import urlencode

from goods.models import Categories

register = template.Library()


@register.simple_tag
def tag_categories():
    return Categories.objects.all()


@register.simple_tag
def change_params(request, **kwargs):
    query = request.GET.copy()
    query.update(kwargs)
    return query.urlencode()
