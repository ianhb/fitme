from django.template import Library

from exercise.models import SetLog, MuscleGroup

register = Library()


@register.filter(name='times')
def times(number):
    return range(1, number + 1)


@register.filter(name='get_sets')
def get_sets(entry):
    return SetLog.objects.filter(log_entry=entry)


@register.simple_tag
def get_muscle_groups():
    return MuscleGroup.objects.all()

