from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from supplementation.models import *

2  # Create your views here.


def supplement_home(request):
    return render(request, 'supplementation/supplement_home.html')


@login_required
def add_supplement(request):
    # TODO
    return render(request, 'supplementation/base.html')


@login_required
def log_supplement_list(request):
    # TODO
    return render(request, 'supplementation/log_supplement_list.html')


@login_required
def log_supplement(request, pk):
    # TODO
    return render(request, 'supplementation/log_supplement.html')


@login_required
def my_supplements(request):
    # TODO
    return render(request, 'supplementation/my_supplements.html')


def search_supplements(request):
    # TODO
    return render(request, 'supplementation/search.html')


def supplement_list(request):
    # TODO

    context = {'supplements': Supplement.objects.all()}

    return render(request, 'supplementation/supplement_list.html', context)


def supplement_detail(request, pk):
    # TODO

    supplement = get_object_or_404(Supplement, pk=pk)

    context = {'supplement': supplement}

    return render(request, 'supplementation/supplement_detail.html', context)


def supplement_category_detail(request, pk):
    # TODO

    category = get_object_or_404(SupplementCategory, pk=pk)

    context = {'category': category}

    return render(request, 'supplementation/category_detail.html', context)
