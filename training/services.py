from datetime import datetime, timedelta
from .models import TrainingPlan, Exercise
import random
from users.models import User

def generate_training_plan(user: User, objetivo: str, dias_por_semana: int = 3):
    from .models import Exercise, TrainingPlan
    if 'fuerza' in objetivo.lower():
        ejercicios = Exercise.objects.filter(category__icontains='fuerza')
    elif 'resistencia' in objetivo.lower():
        ejercicios = Exercise.objects.filter(category__icontains='resistencia')
    elif 'básico' in objetivo.lower() or 'general' in objetivo.lower():
        ejercicios = Exercise.objects.filter(category__icontains='básico') | Exercise.objects.filter(category__icontains='general')
    else:
        ejercicios = Exercise.objects.all()
    ejercicios = list(ejercicios)
    random.shuffle(ejercicios)
    sesiones = []
    ejercicios_por_sesion = max(3, min(6, len(ejercicios)//dias_por_semana))
    for i in range(dias_por_semana):
        inicio = i * ejercicios_por_sesion
        fin = inicio + ejercicios_por_sesion
        sesiones.append(ejercicios[inicio:fin])
    plan = TrainingPlan.objects.create(user=user, name=f"Plan auto-{objetivo}", goals=objetivo)
    from training.models import TrainingSession, ExerciseEntry
    from datetime import date, timedelta
    today = date.today()
    for idx, sesion in enumerate(sesiones):
        session_date = today + timedelta(days=idx)
        ts = TrainingSession.objects.create(training_plan=plan, date=session_date)
        for ex in sesion:
            ExerciseEntry.objects.create(session=ts, exercise=ex, sets=3, reps=10)
    return plan

def calculate_effectiveness_index(plan):
    """
    Calcula un índice de efectividad simple para el plan.
    """
    from training.models import TrainingSession, ExerciseEntry
    sesiones = TrainingSession.objects.filter(training_plan=plan)
    total_ejercicios = sum(ExerciseEntry.objects.filter(session=s).count() for s in sesiones)
    variedad = len(set(ee.exercise_id for s in sesiones for ee in ExerciseEntry.objects.filter(session=s)))
    # Penaliza si hay poca variedad o exceso de volumen
    index = (variedad / max(1, total_ejercicios)) * 100
    if total_ejercicios > 30:
        index -= 10
    if variedad < 5:
        index -= 20
    return max(0, round(index, 1))

def calculate_session_effectiveness(session):
    """
    Calcula el índice de efectividad de una sesión de entrenamiento.
    Ejemplo simple: promedio de (sets * reps * weight) por ejercicio.
    """
    from .models import ExerciseEntry
    entries = ExerciseEntry.objects.filter(session=session)
    if not entries.exists():
        return 0.0
    total = sum(e.sets * e.reps * e.weight for e in entries)
    return total / entries.count()


def update_all_sessions_effectiveness():
    """
    Calcula y guarda el índice de efectividad para todas las sesiones.
    """
    from .models import TrainingSession
    for session in TrainingSession.objects.all():
        session.effectiveness_index = calculate_session_effectiveness(session)
        session.save()


def get_top_sessions_by_effectiveness(top_n=5):
    """
    Devuelve las sesiones con mayor efectividad.
    """
    from .models import TrainingSession
    return TrainingSession.objects.order_by('-effectiveness_index')[:top_n]


def get_avg_effectiveness_by_goal():
    """
    Devuelve el promedio de efectividad por objetivo (goals del plan).
    """
    from .models import TrainingSession
    from django.db.models import Avg
    return (
        TrainingSession.objects.values('training_plan__goals')
        .annotate(avg_effectiveness=Avg('effectiveness_index'))
        .order_by('-avg_effectiveness')
    )


def get_top_goal_by_effectiveness():
    """
    Devuelve el objetivo (goals) con mayor promedio de efectividad.
    """
    avg_by_goal = get_avg_effectiveness_by_goal()
    return avg_by_goal[0] if avg_by_goal else None

class TrainingPlanGenerator:
    def __init__(self, user_profile, training_history, objectives):
        self.user_profile = user_profile
        self.training_history = training_history
        self.objectives = objectives

    def collect_profile_data(self):
        profile_data = {
            'physical_info': getattr(self.user_profile, 'physical_info', None),
            'condition_level': getattr(self.user_profile, 'condition_level', None),
            'restrictions': getattr(self.user_profile, 'restrictions', None),
            'availability': getattr(self.user_profile, 'availability', ['Monday', 'Wednesday', 'Friday']),
        }
        return profile_data

    def define_objectives(self):
        return self.objectives

    def generate_preliminary_plan(self):
        days_available = self.user_profile.availability if hasattr(self.user_profile, 'availability') else ['Monday', 'Wednesday', 'Friday']
        objective_type = self.objectives.get('type', 'strength')

        # Fetch exercises from DB based on objective_type and other criteria
        exercises = Exercise.objects.filter(category__icontains=objective_type)

        # If no exercises found, fallback to all exercises
        if not exercises.exists():
            exercises = Exercise.objects.all()

        selected_exercises = []
        for exercise in exercises[:3]:  # select first 3 exercises for simplicity
            selected_exercises.append({
                "name": exercise.name,
                "sets": 4,
                "reps": 8
            })

        sessions = []
        start_date = datetime.now().date()
        for i, day in enumerate(days_available):
            session_date = start_date + timedelta(days=i*2)
            sessions.append({
                "date": session_date,
                "exercises": selected_exercises
            })

        plan = {
            "sessions": sessions
        }
        return plan

    def calculate_effectiveness_index(self, plan):
        return 0.9

    def optimize_plan(self, plan):
        return plan

    def adjust_plan_dynamic(self, feedback):
        pass

    def create_plan(self):
        profile_data = self.collect_profile_data()
        objectives = self.define_objectives()
        preliminary_plan = self.generate_preliminary_plan()
        effectiveness = self.calculate_effectiveness_index(preliminary_plan)
        optimized_plan = self.optimize_plan(preliminary_plan)
        return optimized_plan
