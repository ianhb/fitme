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
    return render(request, 'supplementation/log_supplement_list.html')


@login_required
def log_supplement(request, pk):
    # TODO
    return render(request, 'supplementation/log_supplement.html')


@login_required
def my_supplements(request):
    # TODO

    all_supps = SupplementLog.objects.filter(user=request.user)

    currents = all_supps.filter(date_ended__isnull=True)
    past = all_supps.filter(date_ended__isnull=False)

    context = {
        'current_supps': currents,
        'past_supps': past
    }

    return render(request, 'supplementation/my_supplements.html', context)


@login_required
def end_log_now(request, pk):
    log = get_object_or_404(SupplementLog, pk=pk)
    log.date_ended = datetime.date.today()
    log.save()
    return HttpResponseRedirect(reverse('my_supplements'))


@login_required
def end_log_set(request, pk):
    # TODO
    log = get_object_or_404(SupplementLog, pk=pk)

    if request.method == 'POST':
        return HttpResponseRedirect(reverse('my_supplements'))

    return render(request, 'supplementation/base.html')


def search_supplements(request):
    # TODO

    supplements = Supplement.objects.all()
    supplement_json = json.dumps(list(supplements.values('pk', 'name', 'category', 'brand')), cls=DjangoJSONEncoder)

    context = {
        'supplements': supplements,
        'supplement_json': supplement_json
    }

    return render(request, 'supplementation/search.html', context)


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

    context = {'category': category,
               'supplements': Supplement.objects.filter(category=category)}

    return render(request, 'supplementation/category_detail.html', context)
