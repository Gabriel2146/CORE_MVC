from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import WgerExercise
from .serializers import WgerExerciseSerializer

class WgerExerciseViewSet(viewsets.ModelViewSet):
    queryset = WgerExercise.objects.all()
    serializer_class = WgerExerciseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='filtered')
    def filtered(self, request):
        user = request.user
        if user.role == 'trainer':
            exercises = WgerExercise.objects.all()
        elif user.role == 'athlete':
            from training.models import TrainingPlan, TrainingSession, ExerciseEntry, Exercise
            plans = TrainingPlan.objects.filter(user=user)
            exercise_ids = set()
            for plan in plans:
                sessions = TrainingSession.objects.filter(training_plan=plan)
                entries = ExerciseEntry.objects.filter(session__in=sessions)
                for entry in entries:
                    if entry.exercise and entry.exercise.wger_id:
                        exercise_ids.add(entry.exercise.wger_id)
            exercises = WgerExercise.objects.filter(wger_id__in=exercise_ids)
        else:
            exercises = WgerExercise.objects.none()
        serializer = self.get_serializer(exercises, many=True)
        return Response(serializer.data)