import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from exercise.models import Routine
from exercise.views.views import illegal_access, get_user_routines


@login_required
def my_routines(request):
    routines = Routine.objects.filter(creator=request.user)

    context = {
        'title': "My Routines",
        'routines': routines
    }

    return render(request, 'exercise/routines/routine_list.html', context)


@login_required
def followed_routines(request):
    routines = Routine.objects.filter(followers=request.user)

    context = {
        'title': "Followed Routines",
        'routines': routines
    }

    return render(request, 'exercise/routines/routine_list.html', context)


def routine_detail(request, pk):
    routine = get_object_or_404(Routine, pk=pk)
    if request.user.is_authenticated() and request.user == routine.creator:

        workouts = routine.workout_set.all().order_by('name')

        context = {
            'routine': routine,
            'workouts': workouts,
        }

        return render(request, 'exercise/routines/routine_detail_creator.html', context)

    elif routine.public:

        workouts = routine.workout_set.all().order_by('name')

        if request.user.is_authenticated():
            followed = routine.followers.filter(pk=request.user.pk).exists()
        else:
            followed = False

        context = {
            'routine': routine,
            'workouts': workouts,
            'followed': followed,
        }

        return render(request, 'exercise/routines/routine_detail_viewer.html', context)

    elif request.user.is_authenticated():
        illegal_access()

    else:
        return redirect_to_login(reverse('routine_detail', kwargs={'pk': pk}))


def search_routines(request):
    routines = get_user_routines(request).annotate(follower_count=Count('followers')).order_by(
        'follower_count').reverse()
    routine_list = list(routines.values('pk', 'name', 'date_created', 'follower_count', 'type', 'difficulty'))
    routine_list = json.dumps(routine_list, cls=DjangoJSONEncoder)

    context = {
        'routines': routines,
        'routine_json': routine_list
    }

    return render(request, 'exercise/routines/routine_search.html', context)


@login_required
def create_routine(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['desc']
        difficulty = request.POST['diff']
        goal = request.POST['type']
        public = request.POST['public']
        routine = Routine(name=name, description=description, creator=request.user, public=public,
                          difficulty=difficulty, type=goal)
        routine.save()
        routine.followers.add(request.user)

        return HttpResponseRedirect(reverse('routine_detail', kwargs={'pk': routine.pk}))

    return render(request, 'exercise/routines/routine_create.html')


@login_required
def follow_routine(request, pk):
    routine = get_object_or_404(Routine, pk=pk)
    if routine.public:
        routine.followers.add(request.user)

        return HttpResponseRedirect(reverse('routine_detail', kwargs={'pk': pk}))
    else:
        illegal_access()


@login_required
def unfollow_routine(request, pk):
    routine = get_object_or_404(Routine, pk=pk)

    if routine.creator != request.user:
        routine.followers.remove(request.user)

    return HttpResponseRedirect(reverse('routine_detail', kwargs={'pk': pk}))
