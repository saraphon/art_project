# orders/templatetags/orders_extras.py
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply value by arg"""
    return value * arg
