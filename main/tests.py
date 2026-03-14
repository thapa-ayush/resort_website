"""
Django unit tests for Diamond Hill Resort models.

Test cases for:
- Room model creation and slug generation
- GalleryImage model creation
- Booking model creation and total calculation
"""

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta
from decimal import Decimal
from .models import Room, GalleryImage, Booking


class RoomModelTest(TestCase):
    """Test cases for the Room model."""

    def setUp(self):
        """Create test room data."""
        self.test_image = SimpleUploadedFile(
            name='test_room.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )

    def tearDown(self):
        """Clean up test image."""
        if self.test_image:
            self.test_image.close()

    def test_room_creation(self):
        """Test creating a room."""
        room = Room.objects.create(
            title='Deluxe Room',
            description='Luxury room with mountain view',
            price=Decimal('12000.00'),
            amenities='WiFi, AC, TV, Private Balcony',
            image=self.test_image
        )

        self.assertEqual(room.title, 'Deluxe Room')
        self.assertEqual(room.price, Decimal('12000.00'))
        self.assertIsNotNone(room.slug)
        self.assertEqual(str(room), 'Deluxe Room')

    def test_slug_auto_generation(self):
        """Test that slug is auto-generated from title."""
        room = Room.objects.create(
            title='Superior Room',
            description='Test room',
            price=Decimal('8000.00'),
            amenities='WiFi, AC',
            image=self.test_image
        )

        self.assertEqual(room.slug, 'superior-room')

    def test_slug_uniqueness(self):
        """Test that slug is unique."""
        Room.objects.create(
            title='Deluxe Room',
            description='Test room',
            price=Decimal('12000.00'),
            amenities='WiFi, AC',
            image=self.test_image
        )

        with self.assertRaises(Exception):
            Room.objects.create(
                title='Deluxe Room',  # Same title should create conflict
                description='Another test room',
                price=Decimal('12000.00'),
                amenities='WiFi, AC',
                image=self.test_image
            )

    def test_amenities_list(self):
        """Test getting amenities as a list."""
        room = Room.objects.create(
            title='Suite',
            description='Luxury suite',
            price=Decimal('15000.00'),
            amenities='WiFi, AC, TV, Mini Bar, Jacuzzi',
            image=self.test_image
        )

        amenities = room.get_amenities_list()
        self.assertEqual(len(amenities), 5)
        self.assertIn('WiFi', amenities)
        self.assertIn('Mini Bar', amenities)

    def test_room_price_validation(self):
        """Test that price is positive."""
        with self.assertRaises(Exception):
            Room.objects.create(
                title='Invalid Room',
                description='Test room',
                price=Decimal('-1000.00'),  # Negative price
                amenities='WiFi',
                image=self.test_image
            )

    def test_absolute_url(self):
        """Test get_absolute_url method."""
        room = Room.objects.create(
            title='Deluxe Room',
            description='Test room',
            price=Decimal('12000.00'),
            amenities='WiFi, AC',
            image=self.test_image
        )

        url = room.get_absolute_url()
        self.assertIn('deluxe-room', url)


class GalleryImageModelTest(TestCase):
    """Test cases for the GalleryImage model."""

    def setUp(self):
        """Create test gallery image."""
        self.test_image = SimpleUploadedFile(
            name='test_gallery.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )

    def tearDown(self):
        """Clean up test image."""
        if self.test_image:
            self.test_image.close()

    def test_gallery_image_creation(self):
        """Test creating a gallery image."""
        image = GalleryImage.objects.create(
            caption='Sunset over Kathmandu valley',
            image=self.test_image
        )

        self.assertEqual(image.caption, 'Sunset over Kathmandu valley')
        self.assertIsNotNone(image.upload_date)
        self.assertEqual(str(image), 'Sunset over Kathmandu valley')

    def test_gallery_image_upload_date(self):
        """Test that upload_date is set automatically."""
        image = GalleryImage.objects.create(
            caption='Test image',
            image=self.test_image
        )

        self.assertIsNotNone(image.upload_date)
        self.assertEqual(image.upload_date.date(), date.today())

    def test_gallery_image_ordering(self):
        """Test that images are ordered by upload_date (newest first)."""
        image1 = GalleryImage.objects.create(
            caption='First image',
            image=self.test_image
        )

        image2 = GalleryImage.objects.create(
            caption='Second image',
            image=self.test_image
        )

        # Query all and check order
        images = list(GalleryImage.objects.all())
        self.assertEqual(images[0].caption, 'Second image')
        self.assertEqual(images[1].caption, 'First image')


class BookingModelTest(TestCase):
    """Test cases for the Booking model."""

    def setUp(self):
        """Create test data."""
        self.test_image = SimpleUploadedFile(
            name='test_room.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )

        self.room = Room.objects.create(
            title='Deluxe Room',
            description='Luxury room',
            price=Decimal('12000.00'),
            amenities='WiFi, AC',
            image=self.test_image
        )

        self.check_in = date.today() + timedelta(days=1)
        self.check_out = date.today() + timedelta(days=3)

    def tearDown(self):
        """Clean up test image."""
        if self.test_image:
            self.test_image.close()

    def test_booking_creation(self):
        """Test creating a booking."""
        booking = Booking.objects.create(
            guest_name='John Doe',
            guest_email='john@example.com',
            guest_phone='+977-1-1234567',
            room=self.room,
            check_in=self.check_in,
            check_out=self.check_out,
            guests=2,
            total_amount=Decimal('48000.00'),
            currency='NPR',
            payment_status='pending'
        )

        self.assertEqual(booking.guest_name, 'John Doe')
        self.assertEqual(booking.room, self.room)
        self.assertEqual(booking.payment_status, 'pending')
        self.assertEqual(booking.currency, 'NPR')

    def test_booking_str_representation(self):
        """Test booking string representation."""
        booking = Booking.objects.create(
            guest_name='John Doe',
            guest_email='john@example.com',
            guest_phone='+977-1-1234567',
            room=self.room,
            check_in=self.check_in,
            check_out=self.check_out,
            guests=2,
            total_amount=Decimal('48000.00')
        )

        self.assertIn('John Doe', str(booking))
        self.assertIn('Deluxe Room', str(booking))

    def test_booking_number_of_nights(self):
        """Test calculating number of nights."""
        booking = Booking.objects.create(
            guest_name='John Doe',
            guest_email='john@example.com',
            guest_phone='+977-1-1234567',
            room=self.room,
            check_in=self.check_in,
            check_out=self.check_out,
            guests=2,
            total_amount=Decimal('48000.00')
        )

        nights = booking.get_number_of_nights()
        self.assertEqual(nights, 2)

    def test_booking_payment_status_choices(self):
        """Test booking payment status choices."""
        statuses = [status[0] for status in Booking.PAYMENT_STATUS_CHOICES]
        self.assertIn('pending', statuses)
        self.assertIn('paid', statuses)
        self.assertIn('cancelled', statuses)
        self.assertIn('confirmed', statuses)

    def test_booking_total_amount_validation(self):
        """Test that total_amount is positive."""
        with self.assertRaises(Exception):
            Booking.objects.create(
                guest_name='John Doe',
                guest_email='john@example.com',
                guest_phone='+977-1-1234567',
                room=self.room,
                check_in=self.check_in,
                check_out=self.check_out,
                guests=2,
                total_amount=Decimal('-1000.00')  # Negative
            )

    def test_booking_guests_validation(self):
        """Test that guests count is at least 1."""
        with self.assertRaises(Exception):
            Booking.objects.create(
                guest_name='John Doe',
                guest_email='john@example.com',
                guest_phone='+977-1-1234567',
                room=self.room,
                check_in=self.check_in,
                check_out=self.check_out,
                guests=0,  # Invalid
                total_amount=Decimal('48000.00')
            )

    def test_booking_email_validation(self):
        """Test that email is properly validated."""
        with self.assertRaises(Exception):
            Booking.objects.create(
                guest_name='John Doe',
                guest_email='invalid-email',  # Invalid email
                guest_phone='+977-1-1234567',
                room=self.room,
                check_in=self.check_in,
                check_out=self.check_out,
                guests=2,
                total_amount=Decimal('48000.00')
            )

    def test_booking_ordering(self):
        """Test that bookings are ordered by creation date (newest first)."""
        booking1 = Booking.objects.create(
            guest_name='John Doe',
            guest_email='john@example.com',
            guest_phone='+977-1-1234567',
            room=self.room,
            check_in=self.check_in,
            check_out=self.check_out,
            guests=2,
            total_amount=Decimal('48000.00')
        )

        booking2 = Booking.objects.create(
            guest_name='Jane Smith',
            guest_email='jane@example.com',
            guest_phone='+977-1-7654321',
            room=self.room,
            check_in=self.check_in + timedelta(days=2),
            check_out=self.check_out + timedelta(days=2),
            guests=1,
            total_amount=Decimal('24000.00')
        )

        bookings = list(Booking.objects.all())
        self.assertEqual(bookings[0].guest_name, 'Jane Smith')
        self.assertEqual(bookings[1].guest_name, 'John Doe')


class BookingIntegrationTest(TestCase):
    """Integration tests for booking creation."""

    def setUp(self):
        """Create test data."""
        self.test_image = SimpleUploadedFile(
            name='test_room.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )

        self.room = Room.objects.create(
            title='Deluxe Room',
            description='Luxury room',
            price=Decimal('12000.00'),
            amenities='WiFi, AC',
            image=self.test_image
        )

    def tearDown(self):
        """Clean up test image."""
        if self.test_image:
            self.test_image.close()

    def test_complete_booking_flow(self):
        """Test complete booking creation flow."""
        check_in = date.today() + timedelta(days=1)
        check_out = date.today() + timedelta(days=4)
        guests = 3
        nights = 3

        # Calculate total
        total = self.room.price * nights * guests

        # Create booking
        booking = Booking.objects.create(
            guest_name='Test User',
            guest_email='test@example.com',
            guest_phone='+977-1-1234567',
            room=self.room,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            total_amount=total,
            payment_status='pending'
        )

        # Verify booking
        self.assertEqual(booking.total_amount, Decimal('108000.00'))
        self.assertEqual(booking.get_number_of_nights(), 3)
        self.assertEqual(booking.payment_status, 'pending')

        # Verify room relationship
        self.assertEqual(booking.room.title, 'Deluxe Room')

        # Update booking status
        booking.payment_status = 'confirmed'
        booking.save()

        # Verify update
        updated_booking = Booking.objects.get(id=booking.id)
        self.assertEqual(updated_booking.payment_status, 'confirmed')
