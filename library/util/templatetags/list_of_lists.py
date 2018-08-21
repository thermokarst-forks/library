from . import register


@register.filter(name='list_of_lists')
def list_of_lists(value, n):
    for i in range(0, len(value), n):
        yield value[i:i + n]
