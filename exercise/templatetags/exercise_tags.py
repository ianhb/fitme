from django.template import Library

from exercise.models import SetLog, MuscleGroup, Equipment

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


@register.simple_tag
def get_equipment():
    return Equipment.objects.all()


@register.filter
def get_item(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return None


@register.simple_tag
def get_log_value(last_log, exercise, set_no, type):
    if exercise in last_log:
        ex_log = last_log[exercise]
        if len(ex_log) > set_no - 1:
            set_log = ex_log[set_no - 1]
            if type in set_log:
                return set_log[type]

    return -1
