import requests
from .models import WgerExercise, SyncLog
from training.models import Exercise

WGER_API_URL = "https://wger.de/api/v2/exercise/"
WGER_CATEGORY_URL = "https://wger.de/api/v2/exercisecategory/"
WGER_EQUIPMENT_URL = "https://wger.de/api/v2/equipment/"

class WgerAPIClient:
    def __init__(self):
        self.session = requests.Session()
        self.category_cache = {}
        self.equipment_cache = {}
    def fetch_exercises(self, language=2, limit=100, offset=0):
        params = {
            'language': language,
            'limit': limit,
            'offset': offset,
            'status': 2
        }
        response = self.session.get(WGER_API_URL, params=params)
        response.raise_for_status()
        return response.json()

    def get_category_name(self, category_id):
        if category_id in self.category_cache:
            return self.category_cache[category_id]
        response = self.session.get(f"{WGER_CATEGORY_URL}{category_id}/")
        if response.status_code == 200:
            data = response.json()
            name = data.get('name', '')
            self.category_cache[category_id] = name
            return name
        return ''

    def get_equipment_names(self, equipment_ids):
        names = []
        for eq_id in equipment_ids:
            if eq_id in self.equipment_cache:
                names.append(self.equipment_cache[eq_id])
                continue
            response = self.session.get(f"{WGER_EQUIPMENT_URL}{eq_id}/")
            if response.status_code == 200:
                data = response.json()
                name = data.get('name', '')
                self.equipment_cache[eq_id] = name
                names.append(name)
        return names

    def fetch_exercise_by_id(self, exercise_id, language=2):
        params = {
            'language': language,
            'status': 2
        }
        response = self.session.get(f"{WGER_API_URL}{exercise_id}/", params=params)
        if response.status_code == 200:
            return response.json()
        return None

    def sync_exercises(self):
        import time
        offset = 0
        limit = 100
        # 1. Importar/actualizar en WgerExercise
        while True:
            data = self.fetch_exercises(limit=limit, offset=offset)
            results = data.get('results', [])
            if not results:
                break
            for item in results:
                name = item.get('name', '')
                description = item.get('description', '')
                # Fallback to English if missing
                if not name or not description:
                    en_item = self.fetch_exercise_by_id(item.get('id'), language=1)
                    if en_item:
                        if not name:
                            name = en_item.get('name', '')
                        if not description:
                            description = en_item.get('description', '')
                category_id = item.get('category', None)
                equipment_ids = item.get('equipment', [])
                category_name = self.get_category_name(category_id) if category_id else ''
                equipment_names = self.get_equipment_names(equipment_ids) if equipment_ids else []
                wger_obj, _ = WgerExercise.objects.update_or_create(
                    wger_id=item.get('id'),
                    defaults={
                        'name': name,
                        'description': description,
                        'category': category_name,
                        'equipment': ', '.join(equipment_names),
                    }
                )
            offset += limit
            if not data.get('next'):
                break
        # 2. Rellenar nombres y descripciones usando la API oficial (como fill_wger_names)
        import requests
        base_url = 'https://wger.de/api/v2/exerciseinfo/'
        for ex in WgerExercise.objects.all():
            if ex.name and ex.description:
                continue
            url = f'{base_url}{ex.wger_id}/?language=2'
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                name = ''
                description = ''
                for t in data.get('translations', []):
                    if t.get('language') == 2:
                        name = t.get('name', '')
                        description = t.get('description', '')
                        break
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
            time.sleep(0.1)  # Para evitar rate limit
        # 3. Copiar a Exercise local
        for w in WgerExercise.objects.all():
            Exercise.objects.update_or_create(
                wger_id=w.wger_id,
                defaults={
                    'name': w.name,
                    'description': w.description,
                    'category': w.category,
                    'muscle_group': w.muscle_group,
                    'difficulty': w.difficulty,
                    'equipment': w.equipment,
                }
            )
        SyncLog.objects.create(action='sync', detail='Sincronización de ejercicios completada')
