from django.core.management.base import BaseCommand
from wger_integration.services import WgerAPIClient

class Command(BaseCommand):
    help = 'Debug sync exercises to print name and description lengths'

    def handle(self, *args, **options):
        client = WgerAPIClient()
        data = client.fetch_exercises()
        for item in data.get('results', []):
            name = item.get('name', '')
            description = item.get('description', '')
            self.stdout.write(f"Exercise name: '{name}', description length: {len(description)}")
