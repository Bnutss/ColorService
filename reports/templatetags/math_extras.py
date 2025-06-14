# В templatetags/math_extras.py (создайте эту папку и файл)
from django import template

register = template.Library()


@register.filter
def sub(value, arg):
    """Subtract the arg from the value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0
