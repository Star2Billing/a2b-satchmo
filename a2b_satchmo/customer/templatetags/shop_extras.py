from django import template
from django.template.defaultfilters import *
from datetime import datetime
from django.contrib.flatpages.models import FlatPage
import operator

register = template.Library()

@register.filter()
def percent(value):
    return str(round(((value * 100)/100), 3)) + " %"


register.filter('percent', percent)

@register.inclusion_tag("footer.html")
def footer_links():
    flatpage_list = FlatPage.objects.all()
    return {'flatpage_list': flatpage_list }
