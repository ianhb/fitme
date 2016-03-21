from django.db.models import Q, Count
from django.shortcuts import render

from exercise.models import Exercise, Workout, Routine, WorkoutLog, ExerciseLog


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


def get_user_routines(request):
    if request.user.is_authenticated():
        return Routine.objects.filter(Q(creator=request.user) | Q(public=True))
    else:
        return Routine.objects.filter(public=True)


def exercise_home(request):
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
