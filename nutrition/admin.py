# Register your models here.
from django.contrib import admin

from nutrition.models import *


class ServingInline(admin.TabularInline):
    model = Serving


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    inlines = (ServingInline,)

admin.site.register(Serving)
admin.site.register(NutritionLog)
admin.site.register(Meal)
admin.site.register(NutritionEntry)
