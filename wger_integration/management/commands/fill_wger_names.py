from django.core.management.base import BaseCommand
from wger_integration.models import WgerExercise
import requests

class Command(BaseCommand):
    help = 'Rellena manualmente los nombres y descripciones de los ejercicios wger usando la API oficial.'

    def handle(self, *args, **options):
        base_url = 'https://wger.de/api/v2/exerciseinfo/'
        total = WgerExercise.objects.count()
        updated = 0
        for ex in WgerExercise.objects.all():
            if ex.name and ex.description:
                continue
            url = f'{base_url}{ex.wger_id}/?language=2'
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                # Buscar traducción en español
                name = ''
                description = ''
                for t in data.get('translations', []):
                    if t.get('language') == 2:
                        name = t.get('name', '')
                        description = t.get('description', '')
                        break
                # Si no hay español, buscar inglés
                if not name or not description:
                    for t in data.get('translations', []):
                        if t.get('language') == 1:
                            if not name:
                                name = t.get('name', '')
                            if not description:
                                description = t.get('description', '')
                if name:
                    ex.name = name
                if description:
                    ex.description = description
                ex.save()
                updated += 1
                self.stdout.write(f'Actualizado ejercicio {ex.wger_id}: {ex.name[:30]}...')
            else:
                self.stdout.write(f'No se pudo obtener info para {ex.wger_id}')
        self.stdout.write(f'Actualizados {updated} de {total} ejercicios.')
