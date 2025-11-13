from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """คูณ value * arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def calc_total(items):
    """รวมราคาสินค้าในตะกร้า"""
    total = 0
    for item in items:
        try:
            price = float(item.product.price) if item.product and item.product.price else 0
            qty = float(item.quantity) if item.quantity else 0
            total += price * qty
        except (ValueError, TypeError, AttributeError):
            continue
    return total
