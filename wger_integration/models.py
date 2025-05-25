from django.db import models

class WgerExercise(models.Model):
    wger_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=255, blank=True)
    muscle_group = models.CharField(max_length=255, blank=True)
    difficulty = models.CharField(max_length=50, blank=True)
    equipment = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class SyncLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
    detail = models.TextField(blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.action}"
