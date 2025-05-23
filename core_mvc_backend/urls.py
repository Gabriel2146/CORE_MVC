from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from users import simple_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/training/', include('training.urls')),
    path('api/wger/', include('wger_integration.urls')),
    path('', simple_views.user_login),
]
