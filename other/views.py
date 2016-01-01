# Create your views here.
from datetime import datetime

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from other.models import FitMeUser, WeightLog, BodyFatLog


def account_home(request):
    return render(request, 'other/home.html')

@login_required
def profile(request):
    user = request.user
    weights = WeightLog.objects.filter(user=user).order_by('date_time').reverse()
    bfs = BodyFatLog.objects.filter(user=user).order_by('date_time').reverse()
    if len(weights) > 0:
        current_weight = weights[0]
    else:
        current_weight = None
    if len(bfs) > 0:
        current_bf = bfs[0]
    else:
        current_bf = None
    height = user.fitmeuser.height
    age = user.fitmeuser.age
    context = {'user': user,
               'current_weight': current_weight,
               'current_body_fat': current_bf,
               'feet': height / 12,
               'inches': height % 12,
               'age': age}

    return render(request, 'other/account.html', context)


@login_required
def new_weight(request):
    if request.method == 'POST':
        updated_weight = request.POST['weight']
        try:
            updated_weight = float(updated_weight)
        except ValueError:
            return render(request, 'other/update_weight.html', {'float_error': True})
        WeightLog(weight=updated_weight, user=request.user, date_time=datetime.now()).save()
        return HttpResponseRedirect(reverse(profile))
    return render(request, 'other/update_weight.html')


@login_required
def new_bf(request):
    if request.method == 'POST':
        updated_body_fat = request.POST['body_fat']
        try:
            updated_body_fat = float(updated_body_fat)
        except ValueError:
            return render(request, 'other/update_body_fat.html', {'float_error': True})
        BodyFatLog(body_fat=updated_body_fat, user=request.user, date_time=datetime.now()).save()
        return HttpResponseRedirect(reverse(profile))
    return render(request, 'other/update_body_fat.html')


def create_account(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            height = (request.POST['height_feet'] * 12) + request.POST['height_inches']
            fitme_data = FitMeUser(user=new_user, height=height, age=request.POST['age'])
            fitme_data.save()
            new_user = auth.authenticate(username=request.POST['username'],
                                         password=request.POST['password1'])
            auth.login(request, new_user)
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserCreationForm()
    return render(request, 'other/create_account.html', {'form': form})
