from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'users/login.html')

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
    if user.role == 'admin':
        return render(request, 'users/dashboard_admin.html')
    elif user.role == 'trainer':
        return render(request, 'users/dashboard_trainer.html')
    elif user.role == 'athlete':
        return render(request, 'users/dashboard_athlete.html')
    elif user.role == 'guest':
        return render(request, 'users/dashboard_guest.html')
    else:
        return HttpResponse("Rol no reconocido")

@login_required
@csrf_exempt
def admin_exercises(request):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    return render(request, 'users/admin_exercises.html')

@login_required
@csrf_exempt
def admin_training_plans(request):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    return render(request, 'users/admin_training_plans.html')

@login_required
@csrf_exempt
def trainer_training_plans(request):
    user = request.user
    if user.role != 'trainer':
        raise PermissionDenied
    return render(request, 'users/trainer_training_plans.html')

@login_required
@csrf_exempt
def athlete_training_plans(request):
    user = request.user
    if user.role != 'athlete':
        raise PermissionDenied
    return render(request, 'users/athlete_training_plans.html')

@login_required
@csrf_exempt
def guest_content(request):
    user = request.user
    if user.role != 'guest':
        raise PermissionDenied
    return render(request, 'users/guest_content.html')
