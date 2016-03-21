import datetime
import json
from operator import itemgetter

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.db.models import Max, F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from exercise.models import Equipment, Exercise, ExerciseLog, SetLog
from exercise.models import MuscleGroup
from exercise.views.views import get_user_exercises


def search_exercises(request):
    exercises = get_user_exercises(request).order_by('name')
    exercises_json = json.dumps(list(exercises.values('pk', 'name', 'muscles_worked', 'equipment')),
                                cls=DjangoJSONEncoder)

    context = {
        'exercises': exercises,
        'exercises_json': exercises_json
    }

    return render(request, 'exercise/exercises/search_exercises.html', context)


def list_exercises(request, filter_type, filter_main, second_filter=None):
    exercises = get_user_exercises(request)
    name = 'all'
    if filter_type == 'muscle' and filter_main != 'all':
        muscle_group_obj = get_object_or_404(MuscleGroup, pk=filter_main)
        exercises = exercises.filter(muscles_worked=muscle_group_obj)
        name = muscle_group_obj.name
    elif filter_type == 'equipment' and filter_main != 'all':
        muscle_group_obj = get_object_or_404(Equipment, pk=filter_main)
        exercises = exercises.filter(equipment=muscle_group_obj)
        name = muscle_group_obj.name
    if second_filter is not None:
        if second_filter == 'top':
            exercises = exercises.order_by('use_count').reverse()
            if exercises.count() < 10:
                exercises = exercises[:exercises.count()]
            else:
                exercises = exercises[:10]

    context = {'exercises': exercises,
               'filter_type': filter_type,
               'filter_main': filter_main,
               'filter_name': name}
    return render(request, 'exercise/exercises/exercise_list.html', context)


def human_readable_date(entry):
    date, weight = entry
    return datetime.date.strftime(date, "%m-%d-%y"), weight


def exercise_detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)

    context = {'exercise': exercise}

    if request.user.is_authenticated():
        exercise_logs = ExerciseLog.objects.filter(log__user=request.user, exercise=exercise)
        if exercise_logs.count() > 0:
            context['logs'] = 'true'
            set_logs = SetLog.objects.filter(log_entry__in=exercise_logs)
            context['last_logged'] = set_logs.order_by('log_entry__log__date').reverse()[0]
            context['max_logged'] = set_logs.order_by('weight').reverse()[0]
            set_logs = set_logs.values('log_entry', 'log_entry__log__date').annotate(
                work_max=Max(F('weight') + (F('weight') * F('reps') * 1.0 / 30.0)))
            daily_maxes = dict()
            for log in set_logs:
                date = log['log_entry__log__date']
                if date in daily_maxes:
                    daily_maxes[date] = max(log['work_max'], daily_maxes[date])
                else:
                    daily_maxes[date] = log['work_max']
            daily_maxes = sorted(daily_maxes.items(), key=itemgetter(0))
            daily_maxes = map(human_readable_date, daily_maxes)
            context['daily_maxes'] = list(daily_maxes)

        else:
            context['logs'] = 'false'
    else:
        context['logs'] = 'false'

    return render(request, 'exercise/exercises/exercise_detail.html', context)


@login_required
def create_exercise(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        exercise = Exercise(name=name, description=description, created_by=request.user)
        exercise.save()
        for group in MuscleGroup.objects.all():
            if request.POST.get('muscles_worked' + str(group.pk)) is not None:
                exercise.muscles_worked.add(group)
        for equip in Equipment.objects.all():
            if request.POST.get('equipment' + str(equip.pk)) is not None:
                exercise.equipment.add(equip)
        return HttpResponseRedirect(reverse('exercise_detail', kwargs={'pk': exercise.pk}))

    context = {'muscle_groups': MuscleGroup.objects.all(),
               'equipment': Equipment.objects.all()}
    return render(request, 'exercise/exercises/create_exercise.html', context)
