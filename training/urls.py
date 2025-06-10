from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExerciseViewSet,
    TrainingPlanViewSet,
    TrainingSessionViewSet,
    ExerciseEntryViewSet,
    update_sessions_effectiveness_view,
    top_sessions_effectiveness_view,
    avg_effectiveness_by_goal_view,
    top_goal_by_effectiveness_view,
    effectiveness_ranking_html_view,
)

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet)
router.register(r'training-plans', TrainingPlanViewSet, basename='trainingplan')
router.register(r'training-sessions', TrainingSessionViewSet)
router.register(r'exercise-entries', ExerciseEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('update-sessions-effectiveness/', update_sessions_effectiveness_view, name='update_sessions_effectiveness'),
    path('top-sessions-effectiveness/', top_sessions_effectiveness_view, name='top_sessions_effectiveness'),
    path('avg-effectiveness-by-goal/', avg_effectiveness_by_goal_view, name='avg_effectiveness_by_goal'),
    path('top-goal-by-effectiveness/', top_goal_by_effectiveness_view, name='top_goal_by_effectiveness'),
    path('effectiveness-ranking/', effectiveness_ranking_html_view, name='effectiveness_ranking_html'),
]
