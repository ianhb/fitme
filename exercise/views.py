# Create your views here.
import datetime
import json
from operator import itemgetter

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.db.models import Count, F, Max, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from exercise.models import Workout, Exercise, MuscleGroup, Equipment, WorkoutEntry, WorkoutLog, ExerciseLog, SetLog


def illegal_access():
    raise Exception("Accessing Illegal Data")


def get_user_exercises(request):
    if request.user.is_authenticated():
        return Exercise.objects.filter(Q(created_by=1) | Q(created_by=request.user))
    else:
        return Exercise.objects.filter(created_by=1)


def get_user_workouts(request):
    if request.user.is_authenticated():
        return Workout.objects.filter(Q(user=request.user) | Q(public=True))
    else:
        return Workout.objects.filter(public=True)


def exercise_home(request):
    # TODO

    if request.user.is_authenticated():
        user_workouts = Workout.objects.filter(user=request.user).order_by('log_count').reverse()

        user_logs = WorkoutLog.objects.filter(user=request.user).order_by('date').reverse()

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
    workouts = Workout.objects.filter(user=request.user).order_by('name')
    return render(request, 'exercise/workout_list.html', {'workouts': workouts})


@login_required
def create_workout(request):
    # TODO
    if request.method == 'POST':
        name = request.POST['name']
        if 'desc_and_notes' in request.POST:
            desc = request.POST['desc_and_notes']
        else:
            desc = ''
        workout = Workout(name=name, user=request.user, public=('public' in request.POST), description=desc)
        workout.save()
        return HttpResponseRedirect(reverse('workout_detail', kwargs={'pk': workout.pk}))

    return render(request, 'exercise/create_workout.html')


@login_required
def record_workout(request, pk=None):
    # TODO

    if pk is None:
        return render(request, 'exercise/select_logged_workout.html',
                      {'workouts': Workout.objects.filter(user=request.user).order_by('log_count')})

    workout = get_object_or_404(Workout, pk=pk)
    entries = WorkoutEntry.objects.filter(workout=workout).order_by('order_in_workout')

    if request.method == 'POST':
        workout_log = WorkoutLog(user=request.user, workout=workout)
        workout_log.date = datetime.datetime.utcnow()
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

    return render(request, 'exercise/log_workout.html', context)


def search_workout(request):
    # TODO

    workouts = get_user_workouts(request).order_by('log_count')
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


def search_exercises(request):
    exercises = get_user_exercises(request).order_by('name')
    exercises_json = json.dumps(list(exercises.values('pk', 'name', 'muscles_worked', 'equipment')),
                                cls=DjangoJSONEncoder)

    context = {
        'exercises': exercises,
        'exercises_json': exercises_json
    }

    return render(request, 'exercise/search_exercises.html', context)


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
    # TODO
    return render(request, 'exercise/exercise_list.html', context)


def human_readable_date(entry):
    date, weight = entry
    return datetime.date.strftime(date, "%m-%d-%y"), weight


def exercise_detail(request, pk):
    # TODO
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
