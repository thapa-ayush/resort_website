"""
Management command to populate room inventory for all room types.
This creates or updates RoomInventory records for existing Room objects.
"""

from django.core.management.base import BaseCommand
from main.models import Room, RoomInventory


class Command(BaseCommand):
    help = 'Populate room inventory for all room types. Set total_rooms to number of each room type available.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total-rooms',
            type=int,
            default=3,
            help='Number of rooms per room type (default: 3)'
        )

    def handle(self, *args, **options):
        total_rooms_per_type = options['total_rooms']
        created_count = 0
        updated_count = 0

        # Get all rooms
        rooms = Room.objects.all()

        if not rooms.exists():
            self.stdout.write(
                self.style.WARNING('❌ No rooms found. Please create rooms first.')
            )
            return

        for room in rooms:
            # Get or create inventory
            inventory, created = RoomInventory.objects.get_or_create(
                room=room,
                defaults={
                    'total_rooms': total_rooms_per_type,
                    'available_rooms': total_rooms_per_type,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Created inventory for {room.title}: {total_rooms_per_type} rooms'
                    )
                )
            else:
                updated_count += 1
                # Optionally update total_rooms if it was 0 or 1
                if inventory.total_rooms <= 1:
                    inventory.total_rooms = total_rooms_per_type
                    inventory.available_rooms = total_rooms_per_type
                    inventory.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Updated inventory for {room.title}: {total_rooms_per_type} rooms'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠️  Inventory already exists for {room.title} ({inventory.total_rooms} rooms), skipping'
                        )
                    )

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Complete! Created {created_count} new inventories, updated {updated_count} existing.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'📦 Total rooms configured: {rooms.count()} room types × {total_rooms_per_type} rooms each'
            )
        )
