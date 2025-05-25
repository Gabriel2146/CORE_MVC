from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from training.forms import ExerciseForm, TrainingPlanForm, ProgressEntryForm
from training.models import TrainingPlan, Exercise, ProgressEntry
from wger_integration.models import WgerExercise, SyncLog
from .models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserChangeForm
import subprocess
from django.contrib import messages
from django import forms
from training.services import generate_training_plan, calculate_effectiveness_index
import csv
from training.models import PlanFeedback

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
    from training.models import Exercise
    from wger_integration.models import WgerExercise
    local_exercises = Exercise.objects.all() if hasattr(Exercise, 'objects') else []
    wger_exercises = WgerExercise.objects.all() if hasattr(WgerExercise, 'objects') else []
    exercises = [
        {'type': 'local', 'obj': e} for e in local_exercises
    ] + [
        {'type': 'wger', 'obj': e} for e in wger_exercises
    ]
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
def admin_exercise_edit(request, exercise_type, pk):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    from training.models import Exercise
    from wger_integration.models import WgerExercise
    from django import forms
    if exercise_type == 'local':
        exercise = get_object_or_404(Exercise, pk=pk)
        if request.method == 'POST':
            form = ExerciseForm(request.POST, instance=exercise)
            if form.is_valid():
                form.save()
                return redirect('users:admin_exercises')
        else:
            form = ExerciseForm(instance=exercise)
        return render(request, 'users/admin_exercise_form.html', {'form': form, 'type': 'local'})
    elif exercise_type == 'wger':
        exercise = get_object_or_404(WgerExercise, pk=pk)
        class ReadOnlyForm(forms.ModelForm):
            class Meta:
                model = WgerExercise
                fields = ['wger_id', 'name', 'description', 'category', 'muscle_group', 'difficulty', 'equipment']
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for field in self.fields.values():
                    field.disabled = True
        form = ReadOnlyForm(instance=exercise)
        return render(request, 'users/admin_exercise_form.html', {'form': form, 'type': 'wger', 'readonly': True})
    else:
        return HttpResponse('Tipo de ejercicio no válido', status=400)

@login_required
@csrf_exempt
def admin_exercise_delete(request, exercise_type, pk):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    from training.models import Exercise
    from wger_integration.models import WgerExercise
    if exercise_type == 'local':
        exercise = get_object_or_404(Exercise, pk=pk)
    elif exercise_type == 'wger':
        exercise = get_object_or_404(WgerExercise, pk=pk)
    else:
        return HttpResponse('Tipo de ejercicio no válido', status=400)
    if request.method == 'POST':
        exercise.delete()
        return redirect('users:admin_exercises')
    return render(request, 'users/admin_exercise_confirm_delete.html', {'exercise': exercise, 'type': exercise_type})

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
    plans = TrainingPlan.objects.filter(trainer=user)
    return render(request, 'users/trainer_training_plans.html', {'plans': plans})

@login_required
@csrf_exempt
def trainer_training_plan_create(request):
    user = request.user
    if user.role != 'trainer':
        raise PermissionDenied
    if request.method == 'POST':
        form = TrainingPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.trainer = user
            plan.save()
            return redirect('users:trainer_training_plans')
    else:
        form = TrainingPlanForm(initial={'trainer': user})
    return render(request, 'users/trainer_training_plan_form.html', {'form': form})

@login_required
@csrf_exempt
def trainer_training_plan_edit(request, pk):
    user = request.user
    if user.role != 'trainer':
        raise PermissionDenied
    plan = get_object_or_404(TrainingPlan, pk=pk, trainer=user)
    if request.method == 'POST':
        form = TrainingPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('users:trainer_training_plans')
    else:
        form = TrainingPlanForm(instance=plan)
    return render(request, 'users/trainer_training_plan_form.html', {'form': form})

@login_required
@csrf_exempt
def trainer_training_plan_delete(request, pk):
    user = request.user
    if user.role != 'trainer':
        raise PermissionDenied
    plan = get_object_or_404(TrainingPlan, pk=pk, trainer=user)
    if request.method == 'POST':
        plan.delete()
        return redirect('users:trainer_training_plans')
    return render(request, 'users/trainer_training_plan_confirm_delete.html', {'plan': plan})

@login_required
@csrf_exempt
def athlete_training_plans(request):
    user = request.user
    if user.role != 'athlete':
        raise PermissionDenied
    plans = TrainingPlan.objects.filter(user=user)
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        comment = request.POST.get('comment')
        if plan_id and comment:
            plan = get_object_or_404(TrainingPlan, pk=plan_id, user=user)
            PlanFeedback.objects.create(plan=plan, user=user, comment=comment)
            messages.success(request, '¡Comentario enviado!')
    feedbacks = {p.id: PlanFeedback.objects.filter(plan=p).order_by('-created_at') for p in plans}
    return render(request, 'users/athlete_training_plans.html', {'plans': plans, 'feedbacks': feedbacks})

@login_required
@csrf_exempt
def guest_content(request):
    user = request.user
    if user.role != 'guest':
        raise PermissionDenied
    from training.models import Exercise
    from wger_integration.models import WgerExercise
    # Mostrar solo ejercicios básicos/públicos: criterio simple = categoría contiene 'básico' o 'general'
    local_exercises = Exercise.objects.filter(category__icontains='básico') | Exercise.objects.filter(category__icontains='general')
    wger_exercises = WgerExercise.objects.filter(category__icontains='basic') | WgerExercise.objects.filter(category__icontains='general')
    exercises = [
        {'type': 'local', 'obj': e} for e in local_exercises
    ] + [
        {'type': 'wger', 'obj': e} for e in wger_exercises
    ]
    return render(request, 'users/guest_content.html', {'exercises': exercises})

@login_required
@csrf_exempt
def trainer_exercises(request):
    user = request.user
    if user.role != 'trainer':
        raise PermissionDenied
    from training.models import Exercise
    from wger_integration.models import WgerExercise
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    local_exercises = Exercise.objects.all()
    wger_exercises = WgerExercise.objects.all()
    if query:
        local_exercises = local_exercises.filter(name__icontains=query)
        wger_exercises = wger_exercises.filter(name__icontains=query)
    if category:
        local_exercises = local_exercises.filter(category__icontains=category)
        wger_exercises = wger_exercises.filter(category__icontains=category)
    exercises = [
        {'type': 'local', 'obj': e} for e in local_exercises
    ] + [
        {'type': 'wger', 'obj': e} for e in wger_exercises
    ]
    return render(request, 'users/trainer_exercises.html', {'exercises': exercises, 'query': query, 'category': category})

@login_required
@csrf_exempt
def athlete_exercises(request):
    user = request.user
    if user.role != 'athlete':
        raise PermissionDenied
    from training.models import Exercise
    from wger_integration.models import WgerExercise
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    # Solo mostrar ejercicios asignados en sus planes
    from training.models import TrainingPlan, TrainingSession, ExerciseEntry
    plans = TrainingPlan.objects.filter(user=user)
    session_ids = TrainingSession.objects.filter(training_plan__in=plans).values_list('id', flat=True)
    entry_ex_ids = ExerciseEntry.objects.filter(session_id__in=session_ids).values_list('exercise_id', flat=True)
    local_exercises = Exercise.objects.filter(id__in=entry_ex_ids)
    wger_ids = local_exercises.values_list('wger_id', flat=True)
    wger_exercises = WgerExercise.objects.filter(wger_id__in=wger_ids)
    if query:
        local_exercises = local_exercises.filter(name__icontains=query)
        wger_exercises = wger_exercises.filter(name__icontains=query)
    if category:
        local_exercises = local_exercises.filter(category__icontains=category)
        wger_exercises = wger_exercises.filter(category__icontains=category)
    exercises = [
        {'type': 'local', 'obj': e} for e in local_exercises
    ] + [
        {'type': 'wger', 'obj': e} for e in wger_exercises
    ]
    return render(request, 'users/athlete_exercises.html', {'exercises': exercises, 'query': query, 'category': category})

@login_required
@csrf_exempt
def exercise_detail(request, exercise_type, pk):
    from training.models import Exercise
    from wger_integration.models import WgerExercise
    if exercise_type == 'local':
        exercise = get_object_or_404(Exercise, pk=pk)
    elif exercise_type == 'wger':
        exercise = get_object_or_404(WgerExercise, pk=pk)
    else:
        return HttpResponse('Tipo de ejercicio no válido', status=400)
    return render(request, 'users/exercise_detail.html', {'exercise': exercise, 'type': exercise_type})

@login_required
def athlete_progress(request):
    user = request.user
    if user.role != 'athlete':
        raise PermissionDenied
    # Obtener ejercicios asignados en los planes del usuario
    from training.models import TrainingPlan, TrainingSession, ExerciseEntry, Exercise
    plans = TrainingPlan.objects.filter(user=user)
    session_ids = TrainingSession.objects.filter(training_plan__in=plans).values_list('id', flat=True)
    entry_ex_ids = ExerciseEntry.objects.filter(session_id__in=session_ids).values_list('exercise_id', flat=True)
    ejercicios = Exercise.objects.filter(id__in=entry_ex_ids).distinct()
    progress_entries = ProgressEntry.objects.filter(user=user).order_by('-date')
    if request.method == 'POST':
        ejercicio_id = request.POST.get('exercise')
        if ejercicio_id:
            ejercicio = Exercise.objects.get(id=ejercicio_id)
            form = ProgressEntryForm(request.POST)
            if form.is_valid():
                entry = form.save(commit=False)
                entry.user = user
                entry.exercise = ejercicio.name
                entry.save()
                return redirect('users:athlete_progress')
        else:
            form = ProgressEntryForm(request.POST)
    else:
        form = ProgressEntryForm()
    return render(request, 'users/athlete_progress.html', {'form': form, 'progress_entries': progress_entries, 'ejercicios': ejercicios})

@login_required
def trainer_athlete_progress(request, athlete_id=None):
    user = request.user
    if user.role != 'trainer':
        raise PermissionDenied
    # Mostrar progreso de todos los deportistas que tienen un plan asignado a este entrenador
    athletes = User.objects.filter(training_plans__trainer=user, role='athlete').distinct()
    selected_athlete = None
    progress_entries = None
    if athlete_id:
        selected_athlete = get_object_or_404(User, pk=athlete_id, role='athlete')
        progress_entries = ProgressEntry.objects.filter(user=selected_athlete).order_by('-date')
    return render(request, 'users/trainer_athlete_progress.html', {
        'athletes': athletes,
        'selected_athlete': selected_athlete,
        'progress_entries': progress_entries
    })

@login_required
def trainer_athlete_progress_graph(request, athlete_id):
    user = request.user
    if user.role != 'trainer':
        raise PermissionDenied
    selected_athlete = get_object_or_404(User, pk=athlete_id, role='athlete')
    entries = ProgressEntry.objects.filter(user=selected_athlete).order_by('date')
    fechas = [e.date.strftime('%Y-%m-%d') for e in entries]
    valores = [getattr(e, 'value', 0) for e in entries]
    import json
    return render(request, 'users/trainer_athlete_progress_graph.html', {
        'fechas': json.dumps(fechas),
        'valores': json.dumps(valores),
        'athlete': selected_athlete
    })

@login_required
@csrf_exempt
def auto_generate_plan(request):
    user = request.user
    if user.role != 'athlete':
        raise PermissionDenied
    plan_preview = None
    effectiveness = None
    sesiones_info = None
    if request.method == 'POST':
        objetivo = request.POST.get('objetivo', 'General')
        dias = int(request.POST.get('dias', 3))
        # Generar plan solo en memoria (no guardar ni asignar)
        plan_preview = generate_training_plan(user, objetivo, dias, preview=True) if 'preview' in generate_training_plan.__code__.co_varnames else generate_training_plan(user, objetivo, dias)
        effectiveness = calculate_effectiveness_index(plan_preview)
        from training.models import TrainingSession, ExerciseEntry
        sesiones = TrainingSession.objects.filter(training_plan=plan_preview).order_by('date') if hasattr(plan_preview, 'id') else []
        sesiones_info = []
        for sesion in sesiones:
            ejercicios = ExerciseEntry.objects.filter(session=sesion)
            sesiones_info.append({
                'fecha': sesion.date,
                'ejercicios': [
                    {'nombre': e.exercise.name, 'sets': e.sets, 'reps': e.reps} for e in ejercicios
                ]
            })
        return render(request, 'users/auto_plan_result.html', {
            'plan': plan_preview,
            'effectiveness': effectiveness,
            'sesiones_info': sesiones_info,
            'solo_preview': True,
            'mensaje': 'Esta es una sugerencia de plan. Contacta a tu entrenador para que lo revise y lo asigne oficialmente.'
        })
    return render(request, 'users/auto_generate_plan.html')

@login_required
def athlete_progress_graph(request):
    user = request.user
    if user.role != 'athlete':
        raise PermissionDenied
    entries = ProgressEntry.objects.filter(user=user).order_by('date')
    fechas = [e.date.strftime('%Y-%m-%d') for e in entries]
    valores = [e.value for e in entries]
    return render(request, 'users/athlete_progress_graph.html', {'fechas': fechas, 'valores': valores})

@login_required
@csrf_exempt
def trainer_auto_generate_plan(request):
    user = request.user
    if user.role != 'trainer':
        raise PermissionDenied
    from users.models import User
    from training.models import TrainingSession, ExerciseEntry, TrainingPlan, Exercise
    athletes = User.objects.filter(training_plans__trainer=user, role='athlete').distinct()
    selected_athlete = None
    plan_preview = None
    effectiveness = None
    sesiones_info = None
    mensaje = None
    asignado = False
    if request.method == 'POST':
        athlete_id = request.POST.get('athlete_id')
        objetivo = request.POST.get('objetivo', 'General')
        dias = int(request.POST.get('dias', 3))
        action = request.POST.get('action', 'preview')
        if athlete_id:
            selected_athlete = User.objects.get(pk=athlete_id, role='athlete')
            if action == 'edit_assign':
                # Edición manual: reconstruir sesiones_info desde POST
                sesiones_info = []
                ejercicios_por_sesion = 0
                # Detectar cuántos ejercicios por sesión hay
                for key in request.POST:
                    if key.startswith('ejercicio_0_'):
                        ejercicios_por_sesion += 1
                for i in range(dias):
                    ejercicios_sesion = []
                    for j in range(ejercicios_por_sesion):
                        nombre = request.POST.get(f'ejercicio_{i}_{j}')
                        sets = int(request.POST.get(f'sets_{i}_{j}', 3))
                        reps = int(request.POST.get(f'reps_{i}_{j}', 10))
                        if nombre:
                            ejercicios_sesion.append({'nombre': nombre, 'sets': sets, 'reps': reps})
                    sesiones_info.append({'fecha': None, 'ejercicios': ejercicios_sesion})
                # Asignar plan real con los datos editados
                plan = TrainingPlan.objects.create(user=selected_athlete, trainer=user, name=f"Plan auto-{objetivo}", goals=objetivo)
                from datetime import date, timedelta
                today = date.today()
                for i, sesion in enumerate(sesiones_info):
                    session_date = today + timedelta(days=i)
                    ts = TrainingSession.objects.create(training_plan=plan, date=session_date)
                    for ej in sesion['ejercicios']:
                        ex = Exercise.objects.filter(name__iexact=ej['nombre']).first()
                        if ex:
                            ExerciseEntry.objects.create(session=ts, exercise=ex, sets=ej['sets'], reps=ej['reps'])
                asignado = True
                mensaje = '¡Plan editado y asignado correctamente al deportista!'
                # Notificación al deportista (Django messages, simulado)
                messages.success(request, f'Se ha asignado un nuevo plan a {selected_athlete.username}.')
                plan_preview = plan
                effectiveness = calculate_effectiveness_index(plan)
                sesiones = TrainingSession.objects.filter(training_plan=plan).order_by('date')
                sesiones_info = []
                for sesion in sesiones:
                    ejercicios_sesion = ExerciseEntry.objects.filter(session=sesion)
                    sesiones_info.append({
                        'fecha': sesion.date,
                        'ejercicios': [
                            {'nombre': e.exercise.name, 'sets': e.sets, 'reps': e.reps} for e in ejercicios_sesion
                        ]
                    })
            else:
                # Selección de ejercicios según objetivo
                if 'fuerza' in objetivo.lower():
                    ejercicios = list(Exercise.objects.filter(category__icontains='fuerza'))
                elif 'resistencia' in objetivo.lower():
                    ejercicios = list(Exercise.objects.filter(category__icontains='resistencia'))
                elif 'básico' in objetivo.lower() or 'general' in objetivo.lower():
                    ejercicios = list(Exercise.objects.filter(category__icontains='básico')) + list(Exercise.objects.filter(category__icontains='general'))
                else:
                    ejercicios = list(Exercise.objects.all())
                # Fallback: si no hay ejercicios para el objetivo, usar todos
                if not ejercicios:
                    ejercicios = list(Exercise.objects.all())
                import random
                random.shuffle(ejercicios)
                ejercicios_por_sesion = max(3, min(6, len(ejercicios)//dias))
                if action == 'assign':
                    # Asignar plan real
                    plan = TrainingPlan.objects.create(user=selected_athlete, trainer=user, name=f"Plan auto-{objetivo}", goals=objetivo)
                    from datetime import date, timedelta
                    today = date.today()
                    for i in range(dias):
                        session_date = today + timedelta(days=i)
                        ts = TrainingSession.objects.create(training_plan=plan, date=session_date)
                        inicio = i * ejercicios_por_sesion
                        fin = inicio + ejercicios_por_sesion
                        for ex in ejercicios[inicio:fin]:
                            ExerciseEntry.objects.create(session=ts, exercise=ex, sets=3, reps=10)
                    asignado = True
                    mensaje = '¡Plan asignado correctamente al deportista!'
                    plan_preview = plan
                    effectiveness = calculate_effectiveness_index(plan)
                    sesiones = TrainingSession.objects.filter(training_plan=plan).order_by('date')
                    sesiones_info = []
                    for sesion in sesiones:
                        ejercicios_sesion = ExerciseEntry.objects.filter(session=sesion)
                        sesiones_info.append({
                            'fecha': sesion.date,
                            'ejercicios': [
                                {'nombre': e.exercise.name, 'sets': e.sets, 'reps': e.reps} for e in ejercicios_sesion
                            ]
                        })
                else:
                    # Solo sugerencia (preview, no guardar en DB)
                    from datetime import date, timedelta
                    today = date.today()
                    sesiones_info = []
                    total_ejercicios = len(ejercicios)
                    if total_ejercicios == 0:
                        mensaje = 'No hay ejercicios disponibles para el objetivo seleccionado. Por favor, sincroniza ejercicios o cambia el objetivo.'
                    for i in range(dias):
                        session_date = today + timedelta(days=i)
                        inicio = i * ejercicios_por_sesion
                        fin = inicio + ejercicios_por_sesion
                        ejercicios_sesion = ejercicios[inicio:fin]
                        # Si no hay suficientes ejercicios, repetir la lista circularmente
                        while len(ejercicios_sesion) < ejercicios_por_sesion and ejercicios:
                            faltan = ejercicios_por_sesion - len(ejercicios_sesion)
                            ejercicios_sesion += ejercicios[:faltan]
                        sesiones_info.append({
                            'fecha': session_date,
                            'ejercicios': [
                                {'nombre': ex.name, 'sets': 3, 'reps': 10} for ex in ejercicios_sesion
                            ] if ejercicios else []
                        })
                    plan_preview = type('PlanPreview', (), {'name': f'Plan auto-{objetivo}', 'goals': objetivo})()
                    effectiveness = 0
                    if not mensaje:
                        mensaje = 'Esta es una sugerencia de plan. Si lo consideras adecuado, puedes asignarlo al deportista.'
    return render(request, 'users/trainer_auto_generate_plan.html', {
        'athletes': athletes,
        'selected_athlete': selected_athlete,
        'plan': plan_preview,
        'effectiveness': effectiveness,
        'sesiones_info': sesiones_info,
        'mensaje': mensaje,
        'asignado': asignado
    })

@login_required
@csrf_exempt
def admin_dashboard(request):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    from users.models import User
    from training.models import TrainingPlan, Exercise
    from wger_integration.models import SyncLog
    # Métricas
    total_users = User.objects.count()
    total_trainers = User.objects.filter(role='trainer').count()
    total_athletes = User.objects.filter(role='athlete').count()
    total_plans = TrainingPlan.objects.count()
    total_exercises = Exercise.objects.count()
    # Historial de sincronización (desde modelo SyncLog)
    sync_logs = SyncLog.objects.order_by('-timestamp')[:20]
    return render(request, 'users/admin_dashboard.html', {
        'total_users': total_users,
        'total_trainers': total_trainers,
        'total_athletes': total_athletes,
        'total_plans': total_plans,
        'total_exercises': total_exercises,
        'sync_logs': sync_logs
    })

@login_required
@csrf_exempt
def export_users_csv(request):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    from users.models import User
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="usuarios.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Username', 'Email', 'Rol', 'Activo'])
    for u in User.objects.all():
        writer.writerow([u.id, u.username, u.email, u.get_role_display(), u.is_active])
    return response

@login_required
@csrf_exempt
def export_exercises_csv(request):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    from training.models import Exercise
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ejercicios.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Descripción', 'Categoría', 'Grupo muscular', 'Dificultad', 'Equipo'])
    for e in Exercise.objects.all():
        writer.writerow([e.id, e.name, e.description, e.category, e.muscle_group, e.difficulty, e.equipment])
    return response

@login_required
@csrf_exempt
def export_plans_csv(request):
    user = request.user
    if user.role != 'admin':
        raise PermissionDenied
    from training.models import TrainingPlan
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="planes.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Usuario', 'Entrenador', 'Fecha creación', 'Objetivos'])
    for p in TrainingPlan.objects.all():
        writer.writerow([p.id, p.name, p.user.username, p.trainer.username if p.trainer else '', p.created_at.strftime('%Y-%m-%d'), p.goals])
    return response

@login_required
def trainer_athlete_plans(request, athlete_id):
    user = request.user
    if user.role != 'trainer':
        raise PermissionDenied
    selected_athlete = get_object_or_404(User, pk=athlete_id, role='athlete')
    plans = TrainingPlan.objects.filter(user=selected_athlete).order_by('-created_at')
    return render(request, 'users/trainer_athlete_plans.html', {
        'athlete': selected_athlete,
        'plans': plans
    })
