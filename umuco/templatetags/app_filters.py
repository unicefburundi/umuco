from django import template

register = template.Library()


@register.filter(name="percentageof")
def percentageof(value, arg):
    try:
        ret = int(value) / int(arg)
        return ret
    except (ValueError, ZeroDivisionError):
        return None
