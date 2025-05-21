from django import template

register = template.Library()

@register.filter
def map(iterable, attr):
    if not iterable:
        return []
    result = []
    for item in iterable:
        value = item
        for key in attr.split('__'):
            value = value.get(key, '')
            if value is None:
                value = ''
        result.append(value)
    return result