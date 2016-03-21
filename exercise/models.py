from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

routine_type = (
    ('M', 'Maintenance'),
    ('B', 'Bulking'),
    ('C', 'Cutting')
)

difficulty = (
    ('B', 'Beginner'),
    ('I', 'Intermediate'),
    ('A', 'Advanced')
)


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
    description = models.TextField(blank=True)
    equipment = models.ManyToManyField(Equipment)
    use_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class Routine(models.Model):
    creator = models.ForeignKey(User, related_name="creator")
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False)
    type = models.CharField(default='M', max_length=1, choices=routine_type)
    difficulty = models.CharField(default='B', max_length=1, choices=difficulty)
    description = models.TextField(blank=True, default='')
    followers = models.ManyToManyField(User, related_name="followers")

    def __unicode__(self):
        return self.name


class Workout(models.Model):
    user = models.ForeignKey(User)
    routine = models.ForeignKey(Routine, blank=True, null=True, default=None)
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    log_count = models.IntegerField(default=0)
    description = models.TextField(blank=True, default='')
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
    notes = models.TextField(default='', blank=True)
    linked_above = models.BooleanField(default=False)

    def __unicode__(self):
        return "Workout: " + self.workout.name + ", Exercise: " + self.exercise.name + ", Order: " + str(
                self.order_in_workout)


class WorkoutLog(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField()
    duration = models.FloatField()
    workout = models.ForeignKey(Workout)

    def __unicode__(self):
        return self.user.username + "_" + self.workout.name + "_" + \
               str(self.date.strftime('%m-%d-%y'))


class ExerciseLog(models.Model):
    log = models.ForeignKey(WorkoutLog, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise)
    order = models.IntegerField()


class SetLog(models.Model):
    log_entry = models.ForeignKey(ExerciseLog, on_delete=models.CASCADE)
    weight = models.FloatField()
    reps = models.IntegerField()
    rest = models.IntegerField()
