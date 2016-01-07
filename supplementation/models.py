from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class ServingSize(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()


class SupplementCategory(models.Model):
    name = models.CharField(max_length=64)


class Supplement(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(SupplementCategory)
    barcode = models.IntegerField(default=0)
    label = models.ImageField(default=None, upload_to="/images/supplement_labels/")
    description = models.TextField()
    serving_sizes = models.ForeignKey(ServingSize)
    use_count = models.IntegerField(default=0)


class SupplementLog(models.Model):
    user = models.ForeignKey(User)
    supplement = models.ForeignKey(Supplement)
    date_started = models.DateTimeField()
    date_ended = models.DateTimeField()
    dosage = models.IntegerField()
    serving_size = models.ForeignKey(ServingSize)
