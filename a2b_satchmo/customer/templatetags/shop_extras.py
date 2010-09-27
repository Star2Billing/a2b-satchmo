from django import template
from django.template.defaultfilters import *
from datetime import datetime
import operator

register = template.Library()

@register.filter()
def percent(value):
    return str(round(((value * 100)/100), 3)) + " %"


register.filter('percent', percent)
