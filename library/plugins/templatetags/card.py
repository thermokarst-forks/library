from . import register


@register.inclusion_tag('plugins/_card.html')
def card(plugin):
    return {'plugin': plugin}
