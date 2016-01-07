from django.template import Library

from supplementation.models import SupplementCategory, Brand

register = Library()


@register.simple_tag
def get_supplement_categories():
    return SupplementCategory.objects.all()


@register.simple_tag
def get_brands():
    return Brand.objects.all()
