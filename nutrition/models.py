from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=255)
    barcode = models.IntegerField(default=0)


class Serving(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    calories = models.IntegerField()
    carbohydrates = models.IntegerField()
    fat = models.IntegerField()
    protein = models.IntegerField()
    vitamin_a = models.IntegerField()
    vitamin_c = models.IntegerField()
    iron = models.IntegerField()
    calcium = models.IntegerField()


class NutritionLog(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField()
    total_calories = models.IntegerField()
    total_carbohydrates = models.IntegerField()
    total_fat = models.IntegerField()
    total_protein = models.IntegerField()
    total_vitamin_a = models.IntegerField()
    total_vitamin_c = models.IntegerField()
    total_iron = models.IntegerField()
    total_calcium = models.IntegerField()


class Meal(models.Model):
    log = models.ForeignKey(NutritionLog, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)


class NutritionEntry(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    number_of_servings = models.FloatField()
    serving = models.ForeignKey(Serving)
