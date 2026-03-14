#!/usr/bin/env python
"""Populate sample data for testing all website features."""
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resort_website.settings')
django.setup()

from main.models import Room, Review
from django.utils import timezone

print("=" * 60)
print("POPULATING SAMPLE DATA")
print("=" * 60)

# Create sample rooms
rooms_data = [
    {
        'title': 'Deluxe Room',
        'description': 'Luxury room with mountain view, king bed, private balcony. Includes complimentary breakfast & WiFi. Features panoramic Himalayan views perfect for sunrise.',
        'price': Decimal('12000.00'),
        'price_usd': Decimal('92.00'),
        'price_eur': Decimal('85.00'),
        'amenities': 'Free WiFi, 24-hour front desk, Spa, Mountain View, Private Balcony, King Bed, Complimentary Breakfast, Flat Screen TV, Mini Bar',
        'max_capacity': 2,
        'size_sqft': 350,
    },
    {
        'title': 'Superior Room',
        'description': 'Comfortable room with modern amenities and valley views. Perfect for couples and small families seeking comfort and style.',
        'price': Decimal('8000.00'),
        'price_usd': Decimal('62.00'),
        'price_eur': Decimal('57.00'),
        'amenities': 'Free WiFi, 24-hour front desk, Flat Screen TV, Modern Bathroom, Air Conditioning, Hot Shower, Scenic Views',
        'max_capacity': 3,
        'size_sqft': 280,
    },
    {
        'title': 'Gallery Suite',
        'description': 'Luxury suite with spacious living area, separate bedroom, and premium amenities. Ideal for families and special occasions with exclusive resort access.',
        'price': Decimal('15000.00'),
        'price_usd': Decimal('115.00'),
        'price_eur': Decimal('106.00'),
        'amenities': 'Free WiFi, 24-hour front desk, Living Room, Separate Bedroom, Premium Toiletries, Room Service, Concierge Service, Rooftop Access, Jacuzzi Tub',
        'max_capacity': 4,
        'size_sqft': 550,
    },
    {
        'title': 'Mountain Retreat Room',
        'description': 'Intimate room nestled in nature with private garden access. Perfect for that peaceful getaway with stunning mountain backdrop.',
        'price': Decimal('10000.00'),
        'price_usd': Decimal('77.00'),
        'price_eur': Decimal('71.00'),
        'amenities': 'Free WiFi, Garden Access, Mountain View, Hot Water, Complimentary Tea, Reading Nook, Nature Sound System',
        'max_capacity': 2,
        'size_sqft': 300,
    },
]

print("\n📝 Creating Rooms...\n")
created_rooms = []
for room_data in rooms_data:
    room, created = Room.objects.get_or_create(
        title=room_data['title'],
        defaults=room_data
    )
    status = "✓ Created" if created else "✓ Already exists"
    print(f"{status}: {room.title} (NPR {room.price})")
    created_rooms.append(room)

# Create sample reviews
reviews_data = [
    {
        'guest_name': 'John Smith',
        'rating': 5,
        'location': 'United States',
        'review_text': 'Absolutely amazing experience! The views are breathtaking and the staff was incredibly helpful. Best resort stay we\'ve had in years. Highly recommended!',
        'is_published': True,
    },
    {
        'guest_name': 'Maria Garcia',
        'rating': 5,
        'location': 'Spain',
        'review_text': 'Diamond Hill Resort exceeded all our expectations. The rooms are clean, comfortable, and the hospitality is outstanding. The breakfast was delicious!',
        'is_published': True,
    },
    {
        'guest_name': 'David Chen',
        'rating': 4,
        'location': 'China',
        'review_text': 'Great location with wonderful mountain views. The rooms are spacious and well-maintained. Only minor issue was the WiFi could be stronger.',
        'is_published': True,
    },
    {
        'guest_name': 'Sophie Laurent',
        'rating': 5,
        'location': 'France',
        'review_text': 'One of the best resorts in Nepal! Professional staff, pristine rooms, and spectacular Himalayan views. Will definitely come back!',
        'is_published': True,
    },
    {
        'guest_name': 'Raj Patel',
        'rating': 4,
        'location': 'India',
        'review_text': 'Perfect getaway during monsoon season. Quiet, peaceful, and the nature around is beautiful. Great value for the price.',
        'is_published': True,
    },
]

print("\n⭐ Creating Reviews...\n")
for review_data in reviews_data:
    review, created = Review.objects.get_or_create(
        guest_name=review_data['guest_name'],
        defaults={**review_data, 'visited_date': timezone.now().date()}
    )
    status = "✓ Created" if created else "✓ Already exists"
    print(f"{status}: {review.guest_name} ({review.rating}★)")

print("\n" + "=" * 60)
print("✓ SAMPLE DATA POPULATION COMPLETE!")
print("=" * 60)

# Print verification
from main.models import Room, Review
print(f"\n📊 Verification:")
print(f"   Rooms in database: {Room.objects.count()}")
print(f"   Reviews in database: {Review.objects.count()}")
print(f"\n✓ Website is ready to display all content!")
print("=" * 60)
