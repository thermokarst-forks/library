from django.utils.text import slugify


def slug(model_instance, slugable_field_name, slug_field_name):
    return slugify(getattr(model_instance, slugable_field_name))
