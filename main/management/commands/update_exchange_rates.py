"""
Management command to update exchange rates from external API.

Usage: python manage.py update_exchange_rates
"""

from django.core.management.base import BaseCommand
from main.currency import update_exchange_rates


class Command(BaseCommand):
    help = 'Update exchange rates from external API'

    def handle(self, *args, **options):
        self.stdout.write('Updating exchange rates...')
        
        if update_exchange_rates():
            self.stdout.write(
                self.style.SUCCESS('✅ Exchange rates updated successfully!')
            )
        else:
            self.stdout.write(
                self.style.ERROR('❌ Failed to update exchange rates. Using default rates.')
            )
