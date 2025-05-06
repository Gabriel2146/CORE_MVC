from rest_framework import viewsets
from .models import Exercise, TrainingPlan, TrainingSession, ExerciseEntry
from .serializers import ExerciseSerializer, TrainingPlanSerializer, TrainingSessionSerializer, ExerciseEntrySerializer

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class TrainingPlanViewSet(viewsets.ModelViewSet):
    queryset = TrainingPlan.objects.all()
    serializer_class = TrainingPlanSerializer

class TrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionSerializer

class ExerciseEntryViewSet(viewsets.ModelViewSet):
    queryset = ExerciseEntry.objects.all()
    serializer_class = ExerciseEntrySerializer
