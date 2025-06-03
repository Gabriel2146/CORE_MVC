from django.core.management.base import BaseCommand
from users.models import User
from training.models import ProgressEntry
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Crea datos de progreso de ejemplo para todos los deportistas (athlete) con los mismos valores para comparar.'

    def handle(self, *args, **kwargs):
        ProgressEntry.objects.all().delete()
        athletes = User.objects.filter(role='athlete')
        ejercicio = 'Chin Up'
        fechas = [
            date(2025, 6, 1),
            date(2025, 6, 2)
        ]
        for idx, athlete in enumerate(athletes):
            peso_inicial = 30 + idx * 2  # Diferente para cada atleta
            peso_final = 50 + idx * 2    # Diferente para cada atleta, siempre mayor
            mejora = ((peso_final - peso_inicial) / peso_inicial) * 100 if peso_inicial else 0
            ProgressEntry.objects.create(
                user=athlete,
                exercise=ejercicio,
                date=fechas[0],
                sets=3,
                reps=10,
                weight=peso_inicial,
                notes=f"Progreso en {ejercicio} el {fechas[0]} (Mejora esperada: {mejora:.2f}%)"
            )
            ProgressEntry.objects.create(
                user=athlete,
                exercise=ejercicio,
                date=fechas[1],
                sets=3,
                reps=10,
                weight=peso_final,
                notes=f"Progreso en {ejercicio} el {fechas[1]} (Mejora esperada: {mejora:.2f}%)"
            )
        self.stdout.write(self.style.SUCCESS('Datos de progreso de ejemplo creados para todos los deportistas en Chin Up con valores distintos y mejora visible.'))
