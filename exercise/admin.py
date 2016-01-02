# Register your models here.
from django.contrib import admin

from exercise.models import *


class ExerciseAdmin(admin.ModelAdmin):
    fields = ['name',
              'description',
              'muscles_worked',
              'equipment']


admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Equipment)
admin.site.register(MuscleGroup)
admin.site.register(Regimen)
admin.site.register(Workout)
admin.site.register(WorkoutEntry)
admin.site.register(ExerciseLog)
admin.site.register(ExerciseEntry)
admin.site.register(ExerciseLine)
