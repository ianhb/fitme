# Register your models here.
from django.contrib import admin

from nutrition.models import *

admin.site.register(Food)
admin.site.register(Serving)
admin.site.register(NutritionLog)
admin.site.register(Meal)
admin.site.register(NutritionEntry)
