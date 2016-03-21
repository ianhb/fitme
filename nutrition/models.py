from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
import exercise.models as exercise_models


class Food(models.Model):
    name = models.CharField(max_length=255)
    barcode = models.IntegerField(default=0)
    calories_per_100g = models.IntegerField()
    carbohydrates_per_100g = models.IntegerField()
    fat_per_100g = models.IntegerField()
    protein_per_100g = models.IntegerField()
    vitamin_a_per_100g = models.IntegerField()
    vitamin_c_per_100g = models.IntegerField()
    iron_per_100g = models.IntegerField()
    calcium_per_100g = models.IntegerField()
    log_count = models.BigIntegerField(default=0)

    def __unicode__(self):
        return self.name


class Serving(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    scalar = models.FloatField()

    def __unicode__(self):
        return self.name


class FoodLog(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(auto_created=True)
    food = models.ForeignKey(Food)
    serving = models.ForeignKey(Serving)
    serving_count = models.FloatField()


class DayLog(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField()
    total_calories = models.IntegerField()
    total_carbohydrates = models.IntegerField()
    total_fat = models.IntegerField()
    total_protein = models.IntegerField()
    total_vitamin_a = models.IntegerField()
    total_vitamin_c = models.IntegerField()
    total_iron = models.IntegerField()
    total_calcium = models.IntegerField()


class Goal(models.Model):
    user = models.ForeignKey(User)
    date_set = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=1, choices=exercise_models.routine_type, default='M')
    calories = models.IntegerField()
    carbohydrates = models.IntegerField()
    fat = models.IntegerField()
    protein = models.IntegerField()
    vitamin_a = models.IntegerField()
    vitamin_c = models.IntegerField()
    iron = models.IntegerField()
    calcium = models.IntegerField()
