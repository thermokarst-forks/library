from . import register


@register.inclusion_tag('utils/_form_field.html')
def form_field(field, outer_class='control'):
    return {'field': field, 'outer_class': outer_class}
