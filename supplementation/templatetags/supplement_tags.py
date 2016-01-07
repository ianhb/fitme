from django.template import Library

from supplementation.models import SupplementCategory

register = Library()


@register.simple_tag
def get_supplement_categories():
    return SupplementCategory.objects.all()
