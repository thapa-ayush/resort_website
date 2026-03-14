"""
Management command to add Google reviews to the database.
"""
from django.core.management.base import BaseCommand
from main.models import Review


class Command(BaseCommand):
    help = 'Add Google reviews from Diamond Hill Resort'

    def handle(self, *args, **options):
        reviews_data = [
            {
                'guest_name': 'Krishna Chtitrakar',
                'location': 'Nepal',
                'rating': 5,
                'review_text': 'Everything was good. Staff were amazing and food was good. We had a comfortable stay and rooms were clean and bed were comfortable & Extra activities from hotel 20 min Hiking hotel to Jante Dhunga, one hours Hiking panauti temple and museum, 1 day by bus and hiking Namobuddha etc. Its good for everyone.',
                'is_published': True,
            },
            {
                'guest_name': 'Raj Bhatt',
                'location': 'Nepal',
                'rating': 5,
                'review_text': 'Had a family holiday, We all enjoyed with Service room and food! Highly recommended for day out at the peaceful hotel.',
                'is_published': True,
            },
            {
                'guest_name': 'Nitesh Gorkhali',
                'location': 'Nepal',
                'rating': 5,
                'review_text': 'Best food...best service. Reasonable price....thank u for ur great hospitality Prem sharma and arjun karki... Most recommended.',
                'is_published': True,
            },
            {
                'guest_name': 'Megan Pentz',
                'location': 'USA',
                'rating': 5,
                'review_text': 'Diamond Hill hosted our big humanitarian group for two weeks while in the area. It was clean and comfortable. Beautiful scenery on top of a forested hill. Check out the fireflies at night while relaxing in the courtyard.',
                'is_published': True,
            },
            {
                'guest_name': 'Retireland',
                'location': 'UK',
                'rating': 4,
                'review_text': 'I arrived at this hotel mid week and the staff were extremely welcoming. It was a pleasure to stay in this hotel. After so much trekking in the daytime the hot bath was so welcoming. The food was tasty and great quality - the chicken for example, was the best quality of my travels in Nepal. I would visit the Diamond resort again if I was in the district.',
                'is_published': True,
            },
        ]

        created_count = 0
        for review_data in reviews_data:
            # Check if review already exists
            existing = Review.objects.filter(
                guest_name=review_data['guest_name'],
                location=review_data['location']
            ).exists()

            if not existing:
                review = Review.objects.create(**review_data)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created review by {review.guest_name} ({review.rating} stars)')
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'⏭️  Review by {review_data["guest_name"]} already exists')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✨ Successfully added {created_count} new reviews!')
        )
