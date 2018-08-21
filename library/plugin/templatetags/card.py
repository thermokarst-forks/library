from . import register


@register.inclusion_tag('plugin/_card.html')
def card(plugin):
    return {'plugin': plugin}
