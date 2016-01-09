import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from supplementation.models import *


# Create your views here.


def supplement_home(request):
    return render(request, 'supplementation/supplement_home.html')


@login_required
def log_supplement_list(request):
    # TODO

    supp_list = Supplement.objects.all()

    context = {
        'supplement_list': supp_list
    }

    return render(request, 'supplementation/log_supplement_list.html', context)


@login_required
def log_supplement(request, pk):
    # TODO

    supplement = get_object_or_404(Supplement, pk=pk)

    if request.method == 'POST':
        if request.POST['start_today']:
            start_date = datetime.date.today()
        else:
            start_date = request.POST['start_date']
        if request.POST['current']:
            if SupplementLog.objects.filter(user=request.user, supplement=supplement, date_ended=None).count() > 0:
                return HttpResponseRedirect(reverse('my_supplements'))
            end_date = None
        elif request.POST['end_today']:
            end_date = datetime.date.today()
        else:
            end_date = request.POST['end_date']

        servings = request.POST['servings']

        supplement.use_count += 1
        supplement.save()

        supplement_log = SupplementLog(user=request.user, date_started=start_date, date_ended=end_date, dosage=servings,
                                       supplement=supplement)
        supplement_log.save()
        return HttpResponseRedirect(reverse('my_supplements'))

    context = {
        'supplement': supplement
    }

    return render(request, 'supplementation/log_supplement.html', context)


@login_required
def my_supplements(request):
    # TODO

    all_supps = SupplementLog.objects.filter(user=request.user)

    currents = all_supps.filter(date_ended__isnull=True)
    past = all_supps.filter(date_ended__isnull=False)

    past_supp_types = past.values('supplement').distinct()
    past_supp_list = []

    for entry in past_supp_types:
        supplement = entry['supplement']
        past_supp_list.append((supplement, Supplement.objects.get(pk=supplement).name,
                               past.filter(supplement=supplement).order_by('date_started').
                               values('date_started', 'date_ended')))

    context = {
        'current_supps': currents,
        'past_supps': past_supp_list
    }

    return render(request, 'supplementation/my_supplements.html', context)


@login_required
def end_log_set(request, pk):
    # TODO
    log = get_object_or_404(SupplementLog, pk=pk)

    if request.method == 'POST':
        if request.POST['today']:
            end_date = datetime.date.today()
        else:
            end_date = request.POST['end_date']

        log.date_ended = end_date
        log.save()
        return HttpResponseRedirect(reverse('my_supplements'))

    context = {
        'log': log,
        'supplement': log.supplement
    }

    return render(request, 'supplementation/end_log.html', context)


def search_supplements(request):
    # TODO

    supplements = Supplement.objects.all().order_by('name')
    supplement_json = json.dumps(list(supplements.values('pk', 'name', 'category', 'brand')), cls=DjangoJSONEncoder)

    context = {
        'supplements': supplements,
        'supplement_json': supplement_json
    }

    return render(request, 'supplementation/search.html', context)


def supplement_list(request):
    # TODO

    context = {'supplements': Supplement.objects.all().order_by('use_count')}

    return render(request, 'supplementation/supplement_list.html', context)


def supplement_detail(request, pk):
    # TODO

    supplement = get_object_or_404(Supplement, pk=pk)

    context = {'supplement': supplement}

    return render(request, 'supplementation/supplement_detail.html', context)


def supplement_category_detail(request, pk):
    # TODO

    category = get_object_or_404(SupplementCategory, pk=pk)

    context = {'category': category,
               'supplements': Supplement.objects.filter(category=category).order_by('use_count')}

    return render(request, 'supplementation/category_detail.html', context)
