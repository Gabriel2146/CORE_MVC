from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('trainer', 'Entrenador'),
        ('athlete', 'Deportista'),
        ('guest', 'Invitado'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Rol')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role',)
