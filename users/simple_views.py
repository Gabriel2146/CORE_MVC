from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from training.forms import ExerciseForm, TrainingPlanForm
from training.models import TrainingPlan
from wger_integration.models import WgerExercise
from .models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserChangeForm
import subprocess
from django.contrib import messages

@login_required
@csrf_exempt
def admin_users(request):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    users = User.objects.all()
    return render(request, 'users/admin_users.html', {'users': users})

@login_required
@csrf_exempt
def admin_user_create(request):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:admin_users')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/admin_user_form.html', {'form': form})

@login_required
@csrf_exempt
def admin_user_edit(request, pk):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect('users:admin_users')
    else:
        form = UserChangeForm(instance=user_obj)
    return render(request, 'users/admin_user_form.html', {'form': form})

@login_required
@csrf_exempt
def admin_user_delete(request, pk):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_obj.delete()
        return redirect('users:admin_users')
    return render(request, 'users/admin_user_confirm_delete.html', {'user_obj': user_obj})

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
    exercises = WgerExercise.objects.all()
    return render(request, 'users/admin_exercises.html', {'exercises': exercises})

@login_required
@csrf_exempt
def sync_wger_exercises(request):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    try:
        # Ejecutar el comando de gestión para sincronizar ejercicios
        subprocess.run(['python', 'manage.py', 'sync_wger_exercises'], check=True)
        messages.success(request, 'Sincronización de ejercicios completada con éxito.')
    except subprocess.CalledProcessError:
        messages.error(request, 'Error durante la sincronización de ejercicios.')
    return redirect('users:admin_exercises')

@login_required
@csrf_exempt
def admin_exercise_create(request):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:admin_exercises')
    else:
        form = ExerciseForm()
    return render(request, 'users/admin_exercise_form.html', {'form': form})

@login_required
@csrf_exempt
def admin_exercise_edit(request, pk):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect('users:admin_exercises')
    else:
        form = ExerciseForm(instance=exercise)
    return render(request, 'users/admin_exercise_form.html', {'form': form})

@login_required
@csrf_exempt
def admin_exercise_delete(request, pk):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    exercise = get_object_or_404(Exercise, pk=pk)
    if request.method == 'POST':
        exercise.delete()
        return redirect('users:admin_exercises')
    return render(request, 'users/admin_exercise_confirm_delete.html', {'exercise': exercise})

@login_required
@csrf_exempt
def admin_training_plans(request):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    plans = TrainingPlan.objects.all()
    return render(request, 'users/admin_training_plans.html', {'plans': plans})

@login_required
@csrf_exempt
def admin_training_plan_create(request):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    if request.method == 'POST':
        form = TrainingPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:admin_training_plans')
    else:
        form = TrainingPlanForm()
    return render(request, 'users/admin_training_plan_form.html', {'form': form})

@login_required
@csrf_exempt
def admin_training_plan_edit(request, pk):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    plan = get_object_or_404(TrainingPlan, pk=pk)
    if request.method == 'POST':
        form = TrainingPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('users:admin_training_plans')
    else:
        form = TrainingPlanForm(instance=plan)
    return render(request, 'users/admin_training_plan_form.html', {'form': form})

@login_required
@csrf_exempt
def admin_training_plan_delete(request, pk):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    plan = get_object_or_404(TrainingPlan, pk=pk)
    if request.method == 'POST':
        plan.delete()
        return redirect('users:admin_training_plans')
    return render(request, 'users/admin_training_plan_confirm_delete.html', {'plan': plan})

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
