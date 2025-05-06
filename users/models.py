from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'admin'
    TRAINER = 'trainer'
    ATHLETE = 'athlete'
    GUEST = 'guest'

    ROLE_CHOICES = [
        (ADMIN, 'Administrator'),
        (TRAINER, 'Trainer'),
        (ATHLETE, 'Athlete'),
        (GUEST, 'Guest'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=GUEST)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
