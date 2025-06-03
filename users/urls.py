from django.urls import path
from . import simple_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegisterView, UserListView, UserProfileView

app_name = 'users'

urlpatterns = [
    path('login/', simple_views.user_login, name='login'),
    path('logout/', simple_views.user_logout, name='logout'),
    path('register/', simple_views.user_register, name='register'),
    path('dashboard/', simple_views.dashboard, name='dashboard'),

    path('register-api/', UserRegisterView.as_view(), name='user-register'),
    path('list-api/', UserListView.as_view(), name='user-list'),
    path('profile-api/', UserProfileView.as_view(), name='user-profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('admin/exercises/', simple_views.admin_exercises, name='admin_exercises'),
    path('admin/exercises/create/', simple_views.admin_exercise_create, name='admin_exercise_create'),
    path('admin/exercises/edit/<int:pk>/', simple_views.admin_exercise_edit, name='admin_exercise_edit'),
    path('admin/exercises/delete/<int:pk>/', simple_views.admin_exercise_delete, name='admin_exercise_delete'),
    path('admin/exercises/edit/<str:type>/<int:pk>/', simple_views.admin_exercise_edit, name='admin_exercise_edit'),
    path('admin/exercises/delete/<str:type>/<int:pk>/', simple_views.admin_exercise_delete, name='admin_exercise_delete'),
    path('admin/exercises/sync/', simple_views.sync_wger_exercises, name='sync_wger_exercises'),

    path('admin/training-plans/', simple_views.admin_training_plans, name='admin_training_plans'),
    path('admin/training-plans/create/', simple_views.admin_training_plan_create, name='admin_training_plan_create'),
    path('admin/training-plans/edit/<int:pk>/', simple_views.admin_training_plan_edit, name='admin_training_plan_edit'),
    path('admin/training-plans/delete/<int:pk>/', simple_views.admin_training_plan_delete, name='admin_training_plan_delete'),

    path('trainer/training-plans/', simple_views.trainer_training_plans, name='trainer_training_plans'),
    path('trainer/training-plans/create/', simple_views.trainer_training_plan_create, name='trainer_training_plan_create'),
    path('trainer/training-plans/edit/<int:pk>/', simple_views.trainer_training_plan_edit, name='trainer_training_plan_edit'),
    path('trainer/training-plans/delete/<int:pk>/', simple_views.trainer_training_plan_delete, name='trainer_training_plan_delete'),

    path('athlete/training-plans/', simple_views.athlete_training_plans, name='athlete_training_plans'),
    path('guest/content/', simple_views.guest_content, name='guest_content'),

    path('trainer/exercises/', simple_views.trainer_exercises, name='trainer_exercises'),
    path('athlete/exercises/', simple_views.athlete_exercises, name='athlete_exercises'),
    path('exercise/<str:exercise_type>/<int:pk>/', simple_views.exercise_detail, name='exercise_detail'),
    path('athlete/progress/', simple_views.athlete_progress, name='athlete_progress'),

    path('admin/users/', simple_views.admin_users, name='admin_users'),
    path('admin/users/create/', simple_views.admin_user_create, name='admin_user_create'),
    path('admin/users/edit/<int:pk>/', simple_views.admin_user_edit, name='admin_user_edit'),
    path('admin/users/delete/<int:pk>/', simple_views.admin_user_delete, name='admin_user_delete'),

    path('trainer/athlete-progress/', simple_views.trainer_athlete_progress, name='trainer_athlete_progress'),
    path('trainer/athlete-progress/<int:athlete_id>/', simple_views.trainer_athlete_progress, name='trainer_athlete_progress_detail'),

    path('athlete/auto-generate-plan/', simple_views.auto_generate_plan, name='auto_generate_plan'),
    path('athlete/progress-graph/', simple_views.athlete_progress_graph, name='athlete_progress_graph'),
    path('trainer/auto-generate-plan/', simple_views.trainer_auto_generate_plan, name='trainer_auto_generate_plan'),

    path('admin/dashboard/', simple_views.admin_dashboard, name='admin_dashboard'),

    path('admin/export/users/', simple_views.export_users_csv, name='export_users_csv'),
    path('admin/export/exercises/', simple_views.export_exercises_csv, name='export_exercises_csv'),
    path('admin/export/plans/', simple_views.export_plans_csv, name='export_plans_csv'),

    path('trainer/athlete/<int:athlete_id>/progress_graph/', simple_views.trainer_athlete_progress_graph, name='trainer_athlete_progress_graph'),
    path('trainer/athlete/<int:athlete_id>/plans/', simple_views.trainer_athlete_plans, name='trainer_athlete_plans'),
    path('trainer/athlete-report/', simple_views.trainer_athlete_report, name='trainer_athlete_report'),
]
