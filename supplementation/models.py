from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class SupplementCategory(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Supplement(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(SupplementCategory)
    brand = models.ForeignKey(Brand)
    barcode = models.IntegerField(default=0)
    label = models.ImageField(default=None, upload_to="/images/supplement_labels/", blank=True)
    description = models.TextField(blank=True)
    standard_serving_size = models.IntegerField()
    serving_unit = models.CharField(max_length=128)
    use_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class SupplementLog(models.Model):
    user = models.ForeignKey(User)
    supplement = models.ForeignKey(Supplement)
    date_started = models.DateField()
    date_ended = models.DateField(blank=True, null=True)
    dosage = models.IntegerField()

    def __unicode__(self):
        return "{0}_{1}_{2}".format(self.user, self.supplement.name, self.date_started.strftime("%m-%d-%y"))