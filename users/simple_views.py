from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .forms import CustomUserCreationForm
from training import models as training_models
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('users:login')

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    role = getattr(user, 'role', 'guest')
    # Render different templates or content based on role
    if role == 'admin':
        return render(request, 'users/dashboard_admin.html', {'user': user})
    elif role == 'trainer':
        return render(request, 'users/dashboard_trainer.html', {'user': user})
    elif role == 'athlete':
        return render(request, 'users/dashboard_athlete.html', {'user': user})
    else:
        return render(request, 'users/dashboard_guest.html', {'user': user})

@login_required
@require_http_methods(["GET"])
def admin_exercises(request):
    if request.user.role != 'admin':
        raise PermissionDenied
    exercises = training_models.Exercise.objects.all()
    return render(request, 'users/admin_exercises.html', {'exercises': exercises})

@login_required
@require_http_methods(["GET"])
def admin_training_plans(request):
    if request.user.role != 'admin':
        raise PermissionDenied
    plans = training_models.TrainingPlan.objects.all()
    return render(request, 'users/admin_training_plans.html', {'plans': plans})

@login_required
@require_http_methods(["GET"])
def trainer_training_plans(request):
    if request.user.role != 'trainer':
        raise PermissionDenied
    plans = training_models.TrainingPlan.objects.filter(user=request.user)
    return render(request, 'users/trainer_training_plans.html', {'plans': plans})

@login_required
@require_http_methods(["GET"])
def athlete_training_plans(request):
    if request.user.role != 'athlete':
        raise PermissionDenied
    plans = training_models.TrainingPlan.objects.filter(user=request.user)
    return render(request, 'users/athlete_training_plans.html', {'plans': plans})

@login_required
@require_http_methods(["GET"])
def guest_content(request):
    if request.user.role != 'guest':
        raise PermissionDenied
    exercises = training_models.Exercise.objects.all()
    return render(request, 'users/guest_content.html', {'exercises': exercises})
