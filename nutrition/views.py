# Create your views here.
from django.shortcuts import render


def nutrition_home(request):
    return render(request, 'base/base.html')
