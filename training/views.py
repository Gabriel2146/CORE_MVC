from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Exercise, TrainingPlan, TrainingSession, ExerciseEntry
from .serializers import ExerciseSerializer, TrainingPlanSerializer, TrainingSessionSerializer, ExerciseEntrySerializer
from .services import (
    TrainingPlanGenerator,
    calculate_session_effectiveness,
    update_all_sessions_effectiveness,
    get_top_sessions_by_effectiveness,
    get_avg_effectiveness_by_goal,
    get_top_goal_by_effectiveness,
)
from users.permissions import IsAdmin, IsTrainer, IsAthlete, IsGuest
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

class TrainingPlanViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return TrainingPlan.objects.all()
        return TrainingPlan.objects.filter(user=user)

    @action(detail=False, methods=['post'], permission_classes=[IsTrainer])
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
    permission_classes = [IsAuthenticated]

class ExerciseEntryViewSet(viewsets.ModelViewSet):
    queryset = ExerciseEntry.objects.all()
    serializer_class = ExerciseEntrySerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_sessions_effectiveness_view(request):
    update_all_sessions_effectiveness()
    return Response({'status': 'Índices de efectividad actualizados'})

@api_view(['GET'])
def top_sessions_effectiveness_view(request):
    top_sessions = get_top_sessions_by_effectiveness(5)
    data = [
        {
            'id': s.id,
            'user': s.training_plan.user.username if hasattr(s.training_plan.user, 'username') else str(s.training_plan.user),
            'goal': s.training_plan.goals,
            'plan': str(s.training_plan),
            'date': s.date,
            'effectiveness_index': s.effectiveness_index,
        } for s in top_sessions
    ]
    return Response({'top_sessions': data})

@api_view(['GET'])
def avg_effectiveness_by_goal_view(request):
    avg_by_goal = get_avg_effectiveness_by_goal()
    data = [
        {
            'goal': g['training_plan__goals'],
            'avg_effectiveness': g['avg_effectiveness'],
        } for g in avg_by_goal
    ]
    return Response({'avg_by_goal': data})

@api_view(['GET'])
def top_goal_by_effectiveness_view(request):
    top_goal = get_top_goal_by_effectiveness()
    if top_goal:
        data = {
            'goal': top_goal['training_plan__goals'],
            'avg_effectiveness': top_goal['avg_effectiveness'],
        }
    else:
        data = None
    return Response({'top_goal': data})

@login_required
def effectiveness_ranking_html_view(request):
    return render(request, 'training/effectiveness_ranking.html')
