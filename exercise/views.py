# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from exercise.models import Workout, Exercise, MuscleGroup


def exercise_home(request):
    # TODO
    return render(request, 'exercise/base.html')


@login_required
def workout_home(request):
    # TODO
    return render(request, 'exercise/base.html')


def workout_detail(request, pk):
    # TODO
    workout = get_object_or_404(Workout, pk=pk)
    return render(request, 'exercise/workout_detail.html', {'workout': workout})


@login_required
def my_workouts(request):
    # TODO
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'exercise/workout_list.html', {'workouts': workouts})


@login_required
def create_workout(request):
    # TODO
    return render(request, 'exercise/base.html')


@login_required
def record_workout(request):
    # TODO
    return render(request, 'exercise/base.html')


def find_workouts(request):
    # TODO
    return render(request, 'exercise/base.html')


def list_exercises(request, muscle_group, filter=None):
    if muscle_group != 'all':
        muscle_group_obj = get_object_or_404(MuscleGroup, name__icontains=muscle_group)
        exercises = Exercise.objects.filter(muscles_worked=muscle_group_obj)
    else:
        exercises = Exercise.objects.all()
    if filter is not None:
        if filter == 'top':
            exercises = exercises.order_by('use_count')
            if exercises.count() < 10:
                exercises = exercises[:exercises.count()]
            else:
                exercises = exercises[:10]

    context = {'exercises': exercises,
               'muscle_group': muscle_group}
    # TODO
    return render(request, 'exercise/exercise_list.html', context)


def exercise_detail(request, pk):
    # TODO
    return render(request, 'exercise/base.html')


@login_required
def create_exercise(request):
    # TODO
    return render(request, 'exercise/base.html')


@login_required
def workout_logs(request):
    # TODO
    return render(request, 'exercise/base.html')
