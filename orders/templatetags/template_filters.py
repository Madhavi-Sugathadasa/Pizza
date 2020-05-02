from django import template
from django.conf import settings

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def times(count):
    return range(1, int(count)+1)

@register.filter
def get_quantity(list_of_dict):
    total_items =0;
    for item in list_of_dict:
        qty = item.get("quantity")
        if qty:
            total_items += qty
    return total_items

@register.filter
def currency_symbol(amount):
    return getattr(settings, "CURRENCY_SYMBOL", None) + "{:.2f}".format(amount)


            
    