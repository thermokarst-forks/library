from . import register


@register.inclusion_tag('plugins/_card.html')
def card(plugin, is_detail=False):
    return {'plugin': plugin, 'is_detail': is_detail}
