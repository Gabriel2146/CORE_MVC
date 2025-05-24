import requests
from .models import WgerExercise

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

    def sync_exercises(self):
        offset = 0
        limit = 100
        while True:
            data = self.fetch_exercises(limit=limit, offset=offset)
            results = data.get('results', [])
            if not results:
                break
            for item in results:
                name = item.get('name', '')
                description = item.get('description', '')
                category_id = item.get('category', None)
                equipment_ids = item.get('equipment', [])

                category_name = self.get_category_name(category_id) if category_id else ''
                equipment_names = self.get_equipment_names(equipment_ids) if equipment_ids else []

                WgerExercise.objects.update_or_create(
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
