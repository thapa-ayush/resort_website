"""
Management command to add sample reviews to the database.
Usage: python manage.py add_sample_reviews
"""

from django.core.management.base import BaseCommand
from main.models import Review


class Command(BaseCommand):
    help = 'Add sample reviews to the database'

    def handle(self, *args, **options):
        # Sample reviews data
        sample_reviews = [
            {
                'guest_name': 'Sarah Johnson',
                'location': 'London, UK',
                'rating': 5,
                'review_text': 'An absolutely stunning resort with breathtaking mountain views. The staff was incredibly hospitable and the rooms were immaculate. Highly recommend for anyone visiting Nepal!',
                'is_published': True,
            },
            {
                'guest_name': 'Rajesh Patel',
                'location': 'New Delhi, India',
                'rating': 5,
                'review_text': 'The best resort experience in Nagarkot! Perfect location for sunrise views, excellent food, and amazing service. Our family had an unforgettable honeymoon.',
                'is_published': True,
            },
            {
                'guest_name': 'Emma Wilson',
                'location': 'Sydney, Australia',
                'rating': 4,
                'review_text': 'Wonderful stay with exceptional amenities. The mountain trekking guides were knowledgeable, and the rooftop dining experience was incredible. Will definitely come back!',
                'is_published': True,
            },
            {
                'guest_name': 'Marcos Rodriguez',
                'location': 'Barcelona, Spain',
                'rating': 5,
                'review_text': 'Magnífico! The views from our room were absolutely breathtaking. We watched the sunrise over the Himalayas every morning. The spa treatment was rejuvenating and the staff made us feel like family.',
                'is_published': True,
            },
            {
                'guest_name': 'Yuki Tanaka',
                'location': 'Tokyo, Japan',
                'rating': 5,
                'review_text': 'This resort exceeded all my expectations! The attention to detail in every aspect is remarkable. From the comfortable beds to the delicious local cuisine, everything was perfect. The hiking trails nearby are spectacular.',
                'is_published': True,
            },
            {
                'guest_name': 'Sophie Martin',
                'location': 'Paris, France',
                'rating': 4,
                'review_text': 'A truly peaceful retreat away from the hustle and bustle of the city. The mountain views are simply mesmerizing. The only minor issue was the WiFi connection, but the staff was very accommodating.',
                'is_published': True,
            },
            {
                'guest_name': 'David Chen',
                'location': 'Singapore',
                'rating': 5,
                'review_text': 'Outstanding hospitality and world-class service! The infinity pool overlooking the valleys is incredible. I spent my evenings watching the sunset with a cold drink in hand. Will definitely return!',
                'is_published': True,
            },
            {
                'guest_name': 'Isabella Costa',
                'location': 'Rio de Janeiro, Brazil',
                'rating': 5,
                'review_text': 'Que resort maravilloso! The natural beauty of the location combined with luxury accommodations is unbeatable. The staff is so warm and welcoming. I felt like royalty during my entire stay.',
                'is_published': True,
            },
            {
                'guest_name': 'Alex Thompson',
                'location': 'Toronto, Canada',
                'rating': 4,
                'review_text': 'Amazing experience! The mountain scenery is breathtaking and the resort facilities are top-notch. The local restaurant serves authentic Nepali cuisine that is absolutely delicious. Highly recommended!',
                'is_published': True,
            },
            {
                'guest_name': 'Priya Sharma',
                'location': 'Mumbai, India',
                'rating': 5,
                'review_text': 'A perfect escape for our anniversary! The romantic setting, candlelit dinners, and personalized service made it unforgettable. The spa treatments were heavenly. Thank you for making our special day so memorable!',
                'is_published': True,
            },
        ]

        # Add reviews to database
        created_count = 0
        for review_data in sample_reviews:
            # Check if review already exists
            existing = Review.objects.filter(
                guest_name=review_data['guest_name'],
                location=review_data['location']
            ).exists()

            if not existing:
                Review.objects.create(**review_data)
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Added review from {review_data['guest_name']}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"⏭️ Skipped duplicate review from {review_data['guest_name']}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✨ Successfully added {created_count} reviews to the database!"
            )
        )
