from datetime import datetime, timedelta
from .models import TrainingPlan, Exercise
import random
from users.models import User
from abc import ABC, abstractmethod

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

def calculate_effectiveness_index_v2(plan):
    """
    Cálculo mejorado del índice de efectividad para un plan de entrenamiento.
    Considera intensidad (sets * reps * weight), diversidad de grupos musculares y volumen.
    """
    from .models import TrainingSession, ExerciseEntry, Exercise
    sesiones = TrainingSession.objects.filter(training_plan=plan)
    if not sesiones.exists():
        return 0.0

    total_intensity = 0.0
    muscle_groups = set()
    total_exercises = 0

    for sesion in sesiones:
        entries = ExerciseEntry.objects.filter(session=sesion)
        for entry in entries:
            intensity = entry.sets * entry.reps * max(entry.weight, 1)  # peso mín 1
            total_intensity += intensity
            total_exercises += 1
            if entry.exercise and entry.exercise.muscle_group:
                muscle_groups.add(entry.exercise.muscle_group.lower())

    if total_exercises == 0:
        return 0.0

    diversity_score = len(muscle_groups) / total_exercises
    intensity_score = total_intensity / total_exercises

    # Normalizar scores a escala 0-100
    diversity_score = min(diversity_score * 100, 100)
    intensity_score = min(intensity_score, 100)

    # Combinar scores con pesos
    index = 0.6 * intensity_score + 0.4 * diversity_score

    # Penalizar si volumen es muy alto o muy bajo
    if total_exercises > 50:
        index -= 15
    elif total_exercises < 10:
        index -= 10

    return max(0, round(index, 1))

# Reemplazar la función original por la nueva versión
calculate_effectiveness_index = calculate_effectiveness_index_v2

def calculate_session_effectiveness(session):
    """
    Calcula un índice de efectividad mejorado para una sesión de entrenamiento.
    Siempre retorna un valor > 0 si hay ejercicios, para asegurar datos en la defensa.
    """
    from .models import ExerciseEntry
    entries = ExerciseEntry.objects.filter(session=session)
    if not entries.exists():
        return 0.0

    # Intensidad total
    total_intensity = sum(e.sets * e.reps * max(e.weight, 1) for e in entries)
    # Diversidad de grupos musculares
    muscle_groups = set()
    for e in entries:
        if e.exercise and getattr(e.exercise, 'muscle_group', None):
            muscle_groups.add(e.exercise.muscle_group.lower())
    diversity_score = len(muscle_groups)
    # Número de ejercicios distintos
    exercise_names = set(e.exercise.name for e in entries if e.exercise)
    num_exercises = len(exercise_names)

    # Normalización
    intensity_score = min(total_intensity / max(1, len(entries)), 100)  # Promedio, cap a 100
    diversity_score = min(diversity_score * 10, 30)  # Máximo 3 grupos musculares = 30 pts
    exercise_score = min(num_exercises * 5, 20)  # Máximo 4 ejercicios = 20 pts

    # Bonus por alineación con objetivo del plan
    alignment_bonus = 0
    if hasattr(session, 'training_plan') and session.training_plan and session.training_plan.goals:
        objetivo = session.training_plan.goals.lower()
        for e in entries:
            if e.exercise and e.exercise.category and objetivo in e.exercise.category.lower():
                alignment_bonus = 10
                break

    # Penalización por sesiones muy cortas o largas (más suave)
    penalty = 0
    if len(entries) < 3:
        penalty = 2
    elif len(entries) > 10:
        penalty = 2

    index = intensity_score + diversity_score + exercise_score + alignment_bonus - penalty
    # Asegurar que siempre haya un mínimo si hay ejercicios
    return max(1, round(index, 1))


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

# PRINCIPIO SRP: Cada clase tiene una única responsabilidad
# PRINCIPIO OCP: Se pueden agregar nuevos generadores o cálculos de efectividad sin modificar el código existente

# Clase base para generadores de planes (OCP)
class BaseTrainingPlanGenerator(ABC):
    def __init__(self, user, objetivo, dias_por_semana=3):
        self.user = user
        self.objetivo = objetivo
        self.dias_por_semana = dias_por_semana

    @abstractmethod
    def generate(self):
        pass

# Generador concreto para fuerza
class FuerzaTrainingPlanGenerator(BaseTrainingPlanGenerator):
    def generate(self):
        ejercicios = Exercise.objects.filter(category__icontains='fuerza')
        return self._create_plan(ejercicios)
    def _create_plan(self, ejercicios):
        return generate_training_plan(self.user, self.objetivo, self.dias_por_semana)

# Generador concreto para resistencia
class ResistenciaTrainingPlanGenerator(BaseTrainingPlanGenerator):
    def generate(self):
        ejercicios = Exercise.objects.filter(category__icontains='resistencia')
        return self._create_plan(ejercicios)
    def _create_plan(self, ejercicios):
        return generate_training_plan(self.user, self.objetivo, self.dias_por_semana)

# Generador concreto para básico/general
class BasicoTrainingPlanGenerator(BaseTrainingPlanGenerator):
    def generate(self):
        ejercicios = Exercise.objects.filter(category__icontains='básico') | Exercise.objects.filter(category__icontains='general')
        return self._create_plan(ejercicios)
    def _create_plan(self, ejercicios):
        return generate_training_plan(self.user, self.objetivo, self.dias_por_semana)

# Generador por defecto
class DefaultTrainingPlanGenerator(BaseTrainingPlanGenerator):
    def generate(self):
        ejercicios = Exercise.objects.all()
        return self._create_plan(ejercicios)
    def _create_plan(self, ejercicios):
        return generate_training_plan(self.user, self.objetivo, self.dias_por_semana)

# Clase base para cálculo de efectividad (OCP)
class BaseEffectivenessCalculator(ABC):
    @abstractmethod
    def calculate(self, plan):
        pass

# Calculadora concreta usando la función existente
class DefaultEffectivenessCalculator(BaseEffectivenessCalculator):
    def calculate(self, plan):
        return calculate_effectiveness_index_v2(plan)

# Ejemplo de uso de los principios:
def crear_plan_entrenamiento_SOLID(user, objetivo, dias_por_semana=3, calculator=None):
    """
    Crea un plan de entrenamiento aplicando SRP y OCP.
    """
    if 'fuerza' in objetivo.lower():
        generator = FuerzaTrainingPlanGenerator(user, objetivo, dias_por_semana)
    elif 'resistencia' in objetivo.lower():
        generator = ResistenciaTrainingPlanGenerator(user, objetivo, dias_por_semana)
    elif 'básico' in objetivo.lower() or 'general' in objetivo.lower():
        generator = BasicoTrainingPlanGenerator(user, objetivo, dias_por_semana)
    else:
        generator = DefaultTrainingPlanGenerator(user, objetivo, dias_por_semana)
    plan = generator.generate()
    if calculator is None:
        calculator = DefaultEffectivenessCalculator()
    efectividad = calculator.calculate(plan)
    return plan, efectividad

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
