# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

import exercise.models
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
        result_foods = Food.objects.filter(name__contains=request.GET['food']).order_by('log_count')
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


def convert_dv_to_mcg(user, a, c, i, ca):

    a = int(a) / 100.0
    c = int(c) / 100.0
    i = int(i) / 100.0
    ca = int(ca) / 100.0

    if user.gender =='F':
        mcg_a = a * 700
        if user.age > 18:
            mcg_c = c * 75
            if user.age > 50:
                mg_iron = i * 8
                mg_calc = ca * 1300
            else:
                mg_iron = i * 18
                mg_calc = ca * 1000
        else:
            mcg_c = c * 65
            mg_iron = i * 15
            mg_calc = ca * 1300

    else:
        mcg_a = a * 900
        if user.age > 18:
            mcg_c = c * 90
            mg_iron = i * 8
            mg_calc = ca * 1000
        else:
            mcg_c = c * 75
            mg_iron = i * 11
            mg_calc = ca * 1300
    return mcg_a, mcg_c, mg_iron, mg_calc


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
        a, c, i, ca = convert_dv_to_mcg(request.user.fitmeuser, vit_a_dv, vit_c_dv, iron_dv, calc_dv)
        for g in Goal.objects.filter(user=request.user, active=True):
            g.active = False
            g.save()

        user_goal = Goal(user=request.user, calories=calories, carbohydrates=carbs, fat=fat, protein=protein,
                         vitamin_a=a, vitamin_c=c, iron=i, calcium=ca)
        if diet_type == 1:
            user_goal.type = 'B'
        else:
            user_goal.type = 'C'
        user_goal.save()
        return HttpResponseRedirect(reverse('view_goals'))

    context = {
        'goals': exercise.models.routine_type,
        'user': request.user,
        'fitme_user': request.user.fitmeuser,
        'feet': request.user.fitmeuser.height / 12,
        'inch': request.user.fitmeuser.height % 12,
    }
    weights = WeightLog.objects.filter(user=request.user)
    bfs = BodyFatLog.objects.filter(user=request.user)

    if weights.count() > 0:
        context['weight'] = weights.order_by('date_time')[0]
    if bfs.count() > 0:
        context['bf'] = bfs.order_by('date_time')[0]

    return render(request, 'nutrition/goals/set.html', context)
