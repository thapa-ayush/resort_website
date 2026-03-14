"""
Management command to update rooms with correct data from Diamond Hill Resort official website.
"""

from django.core.management.base import BaseCommand
from main.models import Room


class Command(BaseCommand):
    help = 'Update rooms with correct Diamond Hill Resort room types'

    def handle(self, *args, **options):
        # Delete existing rooms
        Room.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all existing rooms'))

        # Define the 4 room types from the official website
        rooms_data = [
            {
                'title': 'Jr. Suite',
                'description': 'Cozy junior suite with modern amenities. Perfect for solo travelers and couples.',
                'price': 200.00,
                'amenities': 'Air Conditioning, WiFi, TV, Private Bathroom, Mountain View',
                'size_sqft': 200,
                'max_capacity': 1,
                'image': 'rooms/standard_room.JPG'  # Using existing image
            },
            {
                'title': 'Superior Room',
                'description': 'Spacious superior room with enhanced comfort and premium features.',
                'price': 150.00,
                'amenities': 'Air Conditioning, WiFi, TV, Private Bathroom, Balcony, Mountain View',
                'size_sqft': 300,
                'max_capacity': 2,
                'image': 'rooms/standard_room.JPG'
            },
            {
                'title': 'Deluxe Room',
                'description': 'Elegant deluxe room offering luxury and comfort with stunning views.',
                'price': 120.00,
                'amenities': 'Air Conditioning, WiFi, TV, Private Bathroom, Mountain View',
                'size_sqft': 200,
                'max_capacity': 2,
                'image': 'rooms/standard_room.JPG'
            },
            {
                'title': 'Suite (Namo Buddha)',
                'description': 'Luxurious suite named after the sacred Namo Buddha site. Premium experience with expansive layout and panoramic views.',
                'price': 250.00,
                'amenities': 'Air Conditioning, WiFi, TV, Private Bathroom, Sitting Area, Balcony, Premium Bedding, Mountain View, Himalayan Panorama',
                'size_sqft': 787,
                'max_capacity': 2,
                'image': 'rooms/suite_room.JPG'
            }
        ]

        # Create rooms
        for room_data in rooms_data:
            room = Room.objects.create(**room_data)
            self.stdout.write(
                self.style.SUCCESS(f'Created room: {room.title} - NPR {room.price}/night - {room.size_sqft} sqft - Max {room.max_capacity} guests')
            )

        self.stdout.write(self.style.SUCCESS('Successfully updated all rooms!'))
