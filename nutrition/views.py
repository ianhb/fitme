# Create your views here.
from django.shortcuts import render, get_object_or_404

from nutrition.models import Food, Serving, FoodLog


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


def set_goals(request):
    # TODO
    return render(request, 'nutrition/base.html')
