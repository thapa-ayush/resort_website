"""
Management command to create initial hero section slides.
"""

from django.core.management.base import BaseCommand
from main.models import HeroSection


class Command(BaseCommand):
    help = 'Create initial hero section slides from Diamond Hill Resort'

    def handle(self, *args, **options):
        # Check if slides already exist
        if HeroSection.objects.exists():
            self.stdout.write(self.style.WARNING('Hero slides already exist. Skipping...'))
            return

        # Create initial hero slide
        hero = HeroSection.objects.create(
            title='Welcome to Diamond Hill Resort',
            subtitle='Blessed by Nature',
            description='An invitation for a truly unforgettable, lasting memory combining the very best of luxury and serenity. Experience panoramic Himalayan views, world-class hospitality, and authentic mountain retreat in Nagarkot, Nepal.',
            order=1,
            is_active=True
        )
        self.stdout.write(
            self.style.SUCCESS(f'Created hero slide: {hero.title}')
        )
        self.stdout.write(
            self.style.SUCCESS('Hero slides initialized! You can add up to 6 slides in the admin panel.')
        )
