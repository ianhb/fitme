import json

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from exercise.models import Workout, Routine, WorkoutEntry, Exercise
from exercise.views.views import get_user_workouts, illegal_access


def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    exercise_entries = workout.workoutentry_set.order_by('order_in_workout')
    context = {'workout': workout,
               'exercise_entries': exercise_entries}
    return render(request, 'exercise/workouts/workout_detail.html', context)


@login_required
def my_workouts(request):
    workouts = Workout.objects.filter(user=request.user).order_by('name')
    return render(request, 'exercise/workouts/workout_list.html', {'workouts': workouts})


@login_required
def create_workout(request):
    if request.method == 'POST':
        name = request.POST['name']
        if 'desc_and_notes' in request.POST:
            desc = request.POST['desc_and_notes']
        else:
            desc = ''

        workout = Workout(name=name, user=request.user, public=('public' in request.POST), description=desc)
        if int(request.POST['routine_select']) != -1:
            workout.routine = get_object_or_404(Routine, pk=request.POST['routine_select'])
        workout.save()
        return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': workout.pk}))

    context = {
        'routines': Routine.objects.filter(creator=request.user)
    }

    return render(request, 'exercise/workouts/create_workout.html', context)


def search_workout(request):
    workouts = get_user_workouts(request).order_by('log_count').reverse()
    workout_list = list(workouts.values('pk', 'name', 'date_created', 'log_count'))
    for workout in workout_list:
        exercises = WorkoutEntry.objects.filter(workout=workout['pk'])
        muscle_pks = []
        for exercise in exercises:
            for muscle in exercise.exercise.muscles_worked.all():
                if muscle.pk not in muscle_pks:
                    muscle_pks.append(muscle.pk)
        workout['muscles_worked'] = muscle_pks
    workout_json = json.dumps(workout_list, cls=DjangoJSONEncoder)

    context = {
        'workouts': workouts,
        'workout_json': workout_json
    }

    return render(request, 'exercise/workouts/search_workout.html', context)


def add_ex_to_workout(exercise, workout, sets, reps, rest, notes):
    exercise = get_object_or_404(Exercise, pk=exercise)
    exercise.use_count += 1
    exercise.save()
    WorkoutEntry(exercise=exercise, workout=workout,
                 goal_reps_per_set=reps, goal_sets=sets, goal_rest=rest,
                 order_in_workout=workout.exercise_list.count() + 1, notes=notes).save()


@login_required
def add_to_workout(request, pk):
    if request.method == 'POST':
        workout = get_object_or_404(Workout, pk=request.POST['workout_select'])
        if request.user != workout.user:
            illegal_access()
        sets = request.POST['sets']
        reps = request.POST['reps']
        rest = request.POST['rest']
        notes = request.POST['notes'] if 'notes' in request.POST else ''
        add_ex_to_workout(pk, workout, sets, reps, rest, notes)
        return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': workout.pk}))

    exercise = get_object_or_404(Exercise, pk=pk)

    workouts = Workout.objects.filter(user=request.user)
    context = {'exercise': exercise,
               'workouts': workouts}
    if 'workout' in request.GET and workouts.filter(pk=request.GET['workout']).count() > 0:
        context['default_workout'] = int(request.GET['workout'])

    return render(request, 'exercise/workouts/add_to_workout.html', context)


@login_required
def move_exercise_up(request, pk):
    entry = get_object_or_404(WorkoutEntry, pk=pk)
    if request.user != entry.workout.user:
        illegal_access()
    prior_entry = get_object_or_404(WorkoutEntry, workout=entry.workout, order_in_workout=entry.order_in_workout - 1)
    entry.order_in_workout -= 1
    entry.save()
    prior_entry.order_in_workout += 1
    prior_entry.save()
    return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': entry.workout.pk}))


@login_required
def link(request, pk):
    entry = get_object_or_404(WorkoutEntry, pk=pk)
    if request.user != entry.workout.user:
        illegal_access()
    if not entry.linked_above:
        entry.linked_above = True
        entry.save()
    return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': entry.workout.pk}))


@login_required
def unlink(request, pk):
    entry = get_object_or_404(WorkoutEntry, pk=pk)
    if request.user != entry.workout.user:
        illegal_access()
    if entry.linked_above:
        entry.linked_above = False
        entry.save()
    return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': entry.workout.pk}))


def delete_entry(entry):
    entries = entry.workout.workoutentry_set.all()
    for ent in entries:
        if ent.order_in_workout > entry.order_in_workout:
            ent.order_in_workout -= 1
            ent.save()
    entry.delete()


@login_required
def remove_from_workout(request, pk):
    entry = get_object_or_404(WorkoutEntry, pk=pk)
    if request.user != entry.workout.user:
        illegal_access()
    delete_entry(entry)
    return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': entry.workout.pk}))
