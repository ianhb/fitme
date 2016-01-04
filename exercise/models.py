from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class MuscleGroup(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User)
    muscles_worked = models.ManyToManyField(MuscleGroup)
    description = models.TextField()
    equipment = models.ManyToManyField(Equipment)
    use_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class Workout(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    exercise_list = models.ManyToManyField(Exercise, through='WorkoutEntry',
                                           through_fields=('workout', 'exercise'))

    def __unicode__(self):
        return self.name


class WorkoutEntry(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order_in_workout = models.IntegerField()
    goal_sets = models.IntegerField()
    goal_reps_per_set = models.IntegerField()
    goal_rest = models.IntegerField()

    def __unicode__(self):
        return "Workout: " + self.workout.name + ", Exercise: " + self.exercise.name + ", Order: " + str(
                self.order_in_workout)


class Regimen(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    workouts = models.ManyToManyField(Workout)


class ExerciseLog(models.Model):
    user = models.ForeignKey(User)
    date_started = models.DateTimeField()
    date_ended = models.DateTimeField()
    workout = models.ForeignKey(Workout)


class ExerciseEntry(models.Model):
    log = models.ForeignKey(ExerciseLog, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise)
    order = models.IntegerField()


class ExerciseLine(models.Model):
    log_entry = models.ForeignKey(ExerciseEntry, on_delete=models.CASCADE)
    weight = models.IntegerField()
    reps = models.IntegerField()
    rest = models.IntegerField()
