from django.template import Library

from exercise.models import SetLog, MuscleGroup, Equipment

register = Library()


@register.filter(name='max_times')
def max_times(entries):
    max = entries[0][0].goal_sets
    for entry in entries:
        if entry[0].goal_sets > max:
            max = entry[0].goal_sets
    return range(1, max + 1)


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
def get_log_value(log, set_no, type):
    if log is not None:
        if len(log) > set_no - 1:
            set_log = log[set_no - 1]
            if type in set_log:
                return set_log[type]

    return -1
