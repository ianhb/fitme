# Create your views here.
import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from exercise.models import Workout, Exercise, MuscleGroup, Equipment, WorkoutEntry, WorkoutLog, ExerciseLog, SetLog


def illegal_access():
    raise Exception("Accessing Illegal Data")


def exercise_home(request):
    # TODO

    if request.user.is_authenticated():
        user_workouts = Workout.objects.filter(user=request.user).order_by('log_count').reverse()

        user_logs = WorkoutLog.objects.filter(user=request.user).order_by('date_ended')

        user_exercise_logs = ExerciseLog.objects.filter(log__in=user_logs).annotate(exercise_count=Count('exercise'))

        user_exercises = Exercise.objects.filter(exerciselog__in=user_exercise_logs).annotate(
                count=Count('pk')).order_by('count').reverse()

        context = {
            'workouts': user_workouts,
            'exercises': user_exercises,
            'logs': user_logs
        }

        return render(request, 'exercise/home_authed.html', context)
    else:
        return render(request, 'exercise/base.html')


def workout_detail(request, pk):
    # TODO
    workout = get_object_or_404(Workout, pk=pk)
    exercise_entries = workout.workoutentry_set.order_by('order_in_workout')
    context = {'workout': workout,
               'exercise_entries': exercise_entries}
    return render(request, 'exercise/workout_detail.html', context)


@login_required
def my_workouts(request):
    # TODO
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'exercise/workout_list.html', {'workouts': workouts})


@login_required
def create_workout(request):
    # TODO
    if request.method == 'POST':
        name = request.POST['name']
        workout = Workout(name=name, user=request.user, public=('public' in request.POST))
        workout.save()
        return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': workout.pk}))

    return render(request, 'exercise/create_workout.html')


@login_required
def record_workout(request, pk=None):
    # TODO

    if pk is None:
        return render(request, 'exercise/select_logged_workout.html',
                      {'workouts': Workout.objects.filter(user=request.user)})

    workout = get_object_or_404(Workout, pk=pk)
    entries = WorkoutEntry.objects.filter(workout=workout)

    if request.method == 'POST':
        workout_log = WorkoutLog(user=request.user, workout=workout)
        workout_log.date_started = datetime.datetime.utcnow()
        workout_log.date_ended = datetime.datetime.utcnow()
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
                set = SetLog(weight=weight, reps=reps, rest=rest, log_entry=exercise_log)
                set.save()
                set_count += 1
            if set_count == 0:
                exercise_log.delete()
            else:
                order += 1

        workout.log_count += 1
        workout.save()

        return HttpResponseRedirect(reverse('workout_logs'))

    context = {
        'workout': workout,
        'entries': entries
    }

    return render(request, 'exercise/log_workout.html', context)


def search_workout(request):
    # TODO

    workouts = Workout.objects.filter(public=True).order_by('log_count')
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

    return render(request, 'exercise/search_workout.html', context)


def add_ex_to_workout(exercise, workout, sets, reps, rest):
    exercise = get_object_or_404(Exercise, pk=exercise)
    exercise.use_count += 1
    exercise.save()
    WorkoutEntry(exercise=exercise, workout=workout,
                 goal_reps_per_set=reps, goal_sets=sets, goal_rest=rest,
                 order_in_workout=workout.exercise_list.count() + 1).save()


@login_required
def add_to_workout(request, pk):
    if request.method == 'POST':
        workout = get_object_or_404(Workout, pk=request.POST['workout_select'])
        if request.user != workout.user:
            illegal_access()
        sets = request.POST['sets']
        reps = request.POST['reps']
        rest = request.POST['rest']
        add_ex_to_workout(pk, workout, sets, reps, rest)
        return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': workout.pk}))

    exercise = get_object_or_404(Exercise, pk=pk)

    workouts = Workout.objects.filter(user=request.user)
    context = {'exercise': exercise,
               'workouts': workouts}
    if 'workout' in request.GET and workouts.filter(pk=request.GET['workout']).count() > 0:
        context['default_workout'] = int(request.GET['workout'])

    return render(request, 'exercise/add_to_workout.html', context)


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


def search_exercises(request):
    exercises = Exercise.objects.all().order_by('name')
    exercises_json = json.dumps(list(exercises.values('pk', 'name', 'muscles_worked', 'equipment')),
                                cls=DjangoJSONEncoder)

    context = {
        'exercises': exercises,
        'exercises_json': exercises_json
    }

    return render(request, 'exercise/search_exercises.html', context)


def list_exercises(request, filter_type, filter_main, filter=None):
    if filter_type == 'muscle' and filter_main != 'all':
        muscle_group_obj = get_object_or_404(MuscleGroup, pk=filter_main)
        exercises = Exercise.objects.filter(muscles_worked=muscle_group_obj)
    elif filter_type == 'equipment' and filter_main != 'all':
        muscle_group_obj = get_object_or_404(Equipment, pk=filter_main)
        exercises = Exercise.objects.filter(equipment=muscle_group_obj)
    else:
        exercises = Exercise.objects.all()

    if filter is not None:
        if filter == 'top':
            exercises = exercises.order_by('use_count').reverse()
            if exercises.count() < 10:
                exercises = exercises[:exercises.count()]
            else:
                exercises = exercises[:10]

    context = {'exercises': exercises,
               'filter_type': filter_type,
               'filter_main': filter_main}
    # TODO
    return render(request, 'exercise/exercise_list.html', context)


def exercise_detail(request, pk):
    # TODO
    exercise = get_object_or_404(Exercise, pk=pk)

    context = {'exercise': exercise}

    if request.user.is_authenticated():
        exercise_logs = ExerciseLog.objects.filter(log__user=request.user, exercise=exercise)
        set_logs = SetLog.objects.filter(log_entry__in=exercise_logs)
        context['last_logged'] = set_logs.order_by('log_entry__log__date_started')[0] if set_logs.count() > 0 else None
        context['max_logged'] = set_logs.order_by('weight').reverse()[0] if set_logs.count() > 0 else None

    return render(request, 'exercise/exercise_detail.html', context)


@login_required
def create_exercise(request):
    # TODO
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
    return render(request, 'exercise/create_exercise.html', context)


@login_required
def log_list(request):
    # TODO
    context = {'logs': WorkoutLog.objects.filter(user=request.user)}
    return render(request, 'exercise/log_list.html', context)


@login_required
def log_detail(request, pk):
    # TODO

    log = get_object_or_404(WorkoutLog, pk=pk)

    context = {
        'log': log,
        'exercises': log.exerciselog_set.all(),

    }

    return render(request, 'exercise/log_detail.html', context)
