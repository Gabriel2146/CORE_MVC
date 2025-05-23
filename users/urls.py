from django.urls import path
from . import simple_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegisterView, UserListView, UserProfileView

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
]
