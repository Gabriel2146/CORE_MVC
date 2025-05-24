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
    path('admin/exercises/sync/', simple_views.sync_wger_exercises, name='sync_wger_exercises'),

    path('admin/training-plans/', simple_views.admin_training_plans, name='admin_training_plans'),
    path('admin/training-plans/create/', simple_views.admin_training_plan_create, name='admin_training_plan_create'),
    path('admin/training-plans/edit/<int:pk>/', simple_views.admin_training_plan_edit, name='admin_training_plan_edit'),
    path('admin/training-plans/delete/<int:pk>/', simple_views.admin_training_plan_delete, name='admin_training_plan_delete'),

    path('trainer/training-plans/', simple_views.trainer_training_plans, name='trainer_training_plans'),
    path('athlete/training-plans/', simple_views.athlete_training_plans, name='athlete_training_plans'),
    path('guest/content/', simple_views.guest_content, name='guest_content'),
]
