# Create your views here.
from django.shortcuts import render


def nutrition_home(request):
    return render(request, 'nutrition/base.html')


def search_foods(request):
    # TODO
    return render(request, 'nutrition/base.html')


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
