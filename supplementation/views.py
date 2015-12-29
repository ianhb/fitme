# Create your views here.
from django.shortcuts import render


def supplement_home(request):
    return render(request, 'base/base.html')
