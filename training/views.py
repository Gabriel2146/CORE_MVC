from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Exercise, TrainingPlan, TrainingSession, ExerciseEntry
from .serializers import ExerciseSerializer, TrainingPlanSerializer, TrainingSessionSerializer, ExerciseEntrySerializer
from .services import TrainingPlanGenerator

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class TrainingPlanViewSet(viewsets.ModelViewSet):
    queryset = TrainingPlan.objects.all()
    serializer_class = TrainingPlanSerializer

    @action(detail=False, methods=['post'])
    def generate(self, request):
        user_profile = request.data.get('user_profile')
        training_history = request.data.get('training_history')
        objectives = request.data.get('objectives')

        # For demonstration, we pass the raw data; in real app, fetch user profile and history from DB
        generator = TrainingPlanGenerator(user_profile, training_history, objectives)
        plan = generator.create_plan()

        return Response({'plan': plan}, status=status.HTTP_201_CREATED)

class TrainingSessionViewSet(viewsets.ModelViewSet):
    queryset = TrainingSession.objects.all()
    serializer_class = TrainingSessionSerializer

class ExerciseEntryViewSet(viewsets.ModelViewSet):
    queryset = ExerciseEntry.objects.all()
    serializer_class = ExerciseEntrySerializer
