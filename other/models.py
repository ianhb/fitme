from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

genders = (
    ('M', 'MALE'),
    ('F', 'FEMALE')
)


# Create your models here.
class FitKickUser(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField()
    height = models.IntegerField()
    gender = models.CharField(choices=genders, max_length=1)


class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    weight = models.FloatField()

    def __unicode__(self):
        return str(self.weight)


class BodyFatLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    body_fat = models.FloatField()

    def __unicode__(self):
        return str(self.body_fat)
