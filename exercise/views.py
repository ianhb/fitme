# Create your views here.
from django.shortcuts import render


def exercise_home(request):
    return render(request, 'exercise/base.html')
