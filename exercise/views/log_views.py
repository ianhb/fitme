from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from exercise.models import WorkoutLog, ExerciseLog, SetLog, Workout, WorkoutEntry


@login_required
def record_workout(request, pk=None):
    if pk is None:
        return render(request, 'exercise/logs/select_logged_workout.html',
                      {'workouts': Workout.objects.filter(user=request.user).order_by('log_count')})

    workout = get_object_or_404(Workout, pk=pk)
    entries = WorkoutEntry.objects.filter(workout=workout).order_by('order_in_workout')

    if request.method == 'POST':
        workout_log = WorkoutLog(user=request.user, workout=workout)
        workout_log.date = timezone.now()
        workout_log.duration = 0
        workout_log.save()
        order = 1
        for entry in entries:
            exercise_log = ExerciseLog(exercise=entry.exercise, log=workout_log, order=order)
            exercise_log.save()
            set_count = 0
            for i in range(entry.goal_sets):
                form_key = str(entry.pk) + "_" + str(i + 1) + "_"
                weight = request.POST[form_key + 'weight']
                reps = request.POST[form_key + 'reps']
                rest = request.POST[form_key + 'rest']
                if weight == '' or reps == '' or rest == '':
                    continue
                set_log = SetLog(weight=weight, reps=reps, rest=rest, log_entry=exercise_log)
                set_log.save()
                set_count += 1
            if set_count == 0:
                exercise_log.delete()
            else:
                order += 1

        workout.log_count += 1
        workout.save()

        return HttpResponseRedirect(reverse('workout_logs'))

    set_groups = []
    exercise_log_list = ExerciseLog.objects.filter(log__user=request.user)
    exercise_log_list = exercise_log_list.filter(log__workout=workout)
    exercise_log_list = exercise_log_list.annotate(num_sets=Count('setlog')).order_by('log__date').reverse()

    entry_list = exercise_log_list.filter(exercise=entries[0].exercise)
    entry_list = entry_list.filter(num_sets=entries[0].goal_sets)
    if entry_list.count() > 0:
        set_list = [(entries[0], entry_list[0].setlog_set.values('weight', 'reps', 'rest'))]
    else:
        set_list = [(entries[0], None)]

    for entry in entries[1:]:
        entry_list = exercise_log_list.filter(exercise=entry.exercise)
        entry_list = entry_list.filter(num_sets=entry.goal_sets)
        if entry_list.count() > 0:
            tup = (entry, entry_list[0].setlog_set.values('weight', 'reps', 'rest'))
        else:
            tup = (entry, None)
        if entry.linked_above:
            set_list.append(tup)
        else:
            set_groups.append(set_list)
            set_list = [tup]
    set_groups.append(set_list)

    context = {
        'workout': workout,
        'set_groups': set_groups
    }

    return render(request, 'exercise/logs/log_workout.html', context)


@login_required
def log_list(request):
    context = {'logs': WorkoutLog.objects.filter(user=request.user).order_by('-date')}
    return render(request, 'exercise/logs/log_list.html', context)


@login_required
def log_detail(request, pk):
    log = get_object_or_404(WorkoutLog, pk=pk)

    context = {
        'log': log,
        'exercises': log.exerciselog_set.all(),

    }

    return render(request, 'exercise/logs/log_detail.html', context)
