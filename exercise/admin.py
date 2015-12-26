# Register your models here.
from django.contrib import admin

from exercise.models import *

admin.site.register(Exercise)
admin.site.register(Equipment)
admin.site.register(MuscleGroup)
admin.site.register(Regimen)
admin.site.register(Workout)
admin.site.register(WorkoutEntry)
admin.site.register(ExerciseLog)
admin.site.register(ExerciseEntry)
admin.site.register(ExerciseLine)
