# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

import exercise.models
from nutrition import fatsecret_requester
from nutrition.models import Food, Serving, FoodLog, Goal
from other.models import WeightLog, BodyFatLog


def nutrition_home(request):
    return render(request, 'nutrition/base.html')


def create_food(request):
    # TODO
    return render(request, 'nutrition/base.html')


def food_details(request, pk):
    # TODO

    food = get_object_or_404(Food, pk=pk)
    servings = Serving.objects.filter(food=food)

    context = {
        'food': food,
        'servings': servings
    }

    if request.user.is_authenticated():
        food_logs = FoodLog.objects.filter(user=request.user).filter(food=food)
        context['food_logs'] = food_logs

    return render(request, 'nutrition/foods/details.html', context)


def search_foods(request):
    # TODO

    if request.method == 'GET' and 'food' in request.GET:
        result_foods = fatsecret_requester.search(request.GET['food'])
    else:
        result_foods = None

    context = {
        'result_foods': result_foods
    }

    return render(request, 'nutrition/foods/search.html', context)


def log_foods(request):
    # TODO
    return render(request, 'nutrition/base.html')


def day_log(request):
    # TODO
    return render(request, 'nutrition/base.html')


def week_log(request):
    # TODO
    return render(request, 'nutrition/base.html')


def month_log(request):
    # TODO
    return render(request, 'nutrition/base.html')


def view_goals(request):
    # TODO
    return render(request, 'nutrition/base.html')


@login_required
def set_goals(request):
    # TODO

    if request.method == 'POST':
        calories = request.POST['calorie_goal']
        carbs = request.POST['carb_grams']
        fat = request.POST['fat_grams']
        protein = request.POST['protein_grams']
        vit_a_dv = request.POST['vita']
        vit_c_dv = request.POST['vitc']
        iron_dv = request.POST['iron']
        calc_dv = request.POST['calc']
        diet_type = request.POST['diet_type']
        for g in Goal.objects.filter(user=request.user, active=True):
            g.active = False
            g.save()

        user_goal = Goal(user=request.user, calories=calories, carbohydrates=carbs, fat=fat, protein=protein,
                         vitamin_a=vit_a_dv, vitamin_c=vit_c_dv, iron=iron_dv, calcium=calc_dv)
        if diet_type == 1:
            user_goal.type = 'B'
        else:
            user_goal.type = 'C'
        user_goal.save()
        return HttpResponseRedirect(reverse('view_goals'))

    context = {
        'goals': exercise.models.routine_type,
        'user': request.user,
        'fitkick_user': request.user.fitkickuser,
        'feet': request.user.fitkickuser.height / 12,
        'inch': request.user.fitkickuser.height % 12,
    }
    weights = WeightLog.objects.filter(user=request.user)
    bfs = BodyFatLog.objects.filter(user=request.user)

    if weights.count() > 0:
        context['weight'] = weights.order_by('date_time')[0]
    if bfs.count() > 0:
        context['bf'] = bfs.order_by('date_time')[0]

    return render(request, 'nutrition/goals/set.html', context)
