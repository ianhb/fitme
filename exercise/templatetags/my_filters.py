from django.template import Library

from exercise.models import SetLog

register = Library()


@register.filter(name='times')
def times(number):
    return range(1, number + 1)


@register.filter(name='get_sets')
def get_sets(entry):
    return SetLog.objects.filter(log_entry=entry)
