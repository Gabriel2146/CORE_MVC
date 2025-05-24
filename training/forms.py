from django import forms
from .models import Exercise, TrainingPlan

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['wger_id', 'name', 'description', 'category', 'muscle_group', 'difficulty', 'equipment']

class TrainingPlanForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ['user', 'name', 'goals']
