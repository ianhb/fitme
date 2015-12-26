from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class ServingSize(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()


class Supplement(models.Model):
    name = models.CharField(max_length=255)
    barcode = models.IntegerField(default=0)
    description = models.TextField()
    serving_sizes = models.ManyToManyField(ServingSize)


class SupplementLog(models.Model):
    user = models.ForeignKey(User)
    supplement = models.ForeignKey(Supplement)
    date_started = models.DateTimeField()
    date_ended = models.DateTimeField()
    dosage = models.IntegerField()
    serving_size = models.ForeignKey(ServingSize)
