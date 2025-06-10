from django.db import models
from django.conf import settings
from users.models import User

class Exercise(models.Model):
    wger_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=255, blank=True)
    muscle_group = models.CharField(max_length=255, blank=True)
    difficulty = models.CharField(max_length=50, blank=True)
    equipment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return str(self.name)

class TrainingPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='training_plans')
    trainer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='trainer_plans')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    goals = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} for {self.user.username}"

class TrainingSession(models.Model):
    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    notes = models.TextField(blank=True)
    effectiveness_index = models.FloatField(default=0.0)  # reto campo efectividad 

    def __str__(self):
        return "Session on " + str(self.date) + " for " + str(self.training_plan)

class ExerciseEntry(models.Model):
    session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE, related_name='exercise_entries')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(default=0)
    reps = models.IntegerField(default=0)
    weight = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.exercise) + " in session " + str(self.session)

class ProgressEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress_entries')
    exercise = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    sets = models.IntegerField(default=0)
    reps = models.IntegerField(default=0)
    weight = models.FloatField(default=0.0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} - {self.exercise} ({self.date})"

class PlanFeedback(models.Model):
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback de {self.user.username} para {self.plan.name}"
