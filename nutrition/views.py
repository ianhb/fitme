# Create your views here.
from django.shortcuts import render

from nutrition.models import Food


def nutrition_home(request):
    return render(request, 'nutrition/base.html')


def create_food(request):
    # TODO
    return render(request, 'nutrition/base.html')


def food_details(request, pk):
    # TODO
    return render(request, 'nutrition/base.html')


def search_foods(request):
    # TODO

    if request.method == 'GET' and 'food' in request.GET:
        result_foods = Food.objects.filter(name__contains=request.GET['food'])
    else:
        result_foods = None

    context = {
        'result_foods': result_foods
    }

    return render(request, 'nutrition/search.html', context)


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
