# Register your models here.
from django.contrib import admin

from exercise.models import *


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    fields = ['name',
              'description',
              'muscles_worked',
              'equipment',
              'created_by']
    ordering = ('name',)


class ExerciseInline(admin.TabularInline):
    model = Workout.exercise_list.through


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    inlines = (ExerciseInline,)


class ExerciseLogInline(admin.TabularInline):
    model = ExerciseLog


@admin.register(WorkoutLog)
class LogAdmin(admin.ModelAdmin):
    fields = ['user',
              'date',
              'workout']
    inlines = (ExerciseLogInline,)


class SetLogInline(admin.TabularInline):
    model = SetLog


@admin.register(ExerciseLog)
class ExerciseLogAdmin(admin.ModelAdmin):
    inlines = (SetLogInline,)


admin.site.register(Equipment)
admin.site.register(MuscleGroup)
admin.site.register(Regimen)
admin.site.register(WorkoutEntry)
