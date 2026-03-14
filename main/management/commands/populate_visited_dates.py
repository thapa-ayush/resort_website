"""
Management command to populate visited dates for reviews based on created_at date.
"""
from django.core.management.base import BaseCommand
from main.models import Review


class Command(BaseCommand):
    help = 'Populate visited_date field for reviews using created_at date'

    def handle(self, *args, **options):
        reviews = Review.objects.filter(visited_date__isnull=True)
        updated_count = 0

        for review in reviews:
            # Use the created_at date as the visited_date
            review.visited_date = review.created_at.date()
            review.save()
            updated_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Updated {review.guest_name} - Visited date: {review.visited_date}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(f'\n✨ Successfully updated {updated_count} review(s) with visited dates!')
        )
