"""
Django models for Diamond Hill Resort.

Models:
- Room: Defines resort room types with pricing and amenities.
- GalleryImage: Stores gallery images with captions.
- Booking: Manages guest bookings and payment status.
"""

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, EmailValidator
from django.utils import timezone


class Room(models.Model):
    """
    Model representing a room type at the resort.
    
    Fields:
        title (str): Name of the room type (e.g., 'Deluxe Room').
        slug (str): URL-friendly identifier, auto-populated from title.
        description (str): Detailed description of the room.
        price (Decimal): Price per night in NPR.
        amenities (str): JSON or text list of amenities.
        image (ImageField): Room photo.
        size_sqft (int): Room size in square feet.
        max_capacity (int): Maximum number of guests.
        created_at (DateTime): Timestamp when room was added.
        updated_at (DateTime): Timestamp when room was last updated.
    """
    
    title = models.CharField(
        max_length=100,
        unique=True,
        help_text="Room type name (e.g., 'Deluxe Room')"
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text="Auto-generated URL slug"
    )
    description = models.TextField(
        help_text="Detailed room description including features"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Price per night in NPR"
    )
    price_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        help_text="Price per night in USD (auto-calculated or set manually)"
    )
    price_eur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0,
        help_text="Price per night in EUR (auto-calculated or set manually)"
    )
    amenities = models.TextField(
        help_text="Comma-separated list of amenities (e.g., WiFi, AC, TV)"
    )
    image = models.ImageField(
        upload_to='rooms/',
        help_text="Room image"
    )
    size_sqft = models.IntegerField(
        default=200,
        validators=[MinValueValidator(1)],
        help_text="Room size in square feet"
    )
    max_capacity = models.IntegerField(
        default=2,
        validators=[MinValueValidator(1)],
        help_text="Maximum number of guests"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['title']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
    
    def __str__(self):
        """Return room title."""
        return self.title
    
    def save(self, *args, **kwargs):
        """Auto-populate slug from title if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Return the URL for viewing room details."""
        return reverse('main:room_detail', kwargs={'slug': self.slug})
    
    def get_amenities_list(self):
        """Return amenities as a list."""
        return [a.strip() for a in self.amenities.split(',')]
    
    def get_price_by_currency(self, currency='NPR'):
        """
        Get room price in specified currency.
        
        Args:
            currency (str): 'NPR', 'USD', or 'EUR'
            
        Returns:
            Decimal: Price in specified currency
        """
        currency = currency.upper()
        if currency == 'USD':
            return self.price_usd if self.price_usd > 0 else self.price / 130  # Approx conversion
        elif currency == 'EUR':
            return self.price_eur if self.price_eur > 0 else self.price / 140  # Approx conversion
        else:
            return self.price
    
    def get_currency_symbol(self, currency='NPR'):
        """Get currency symbol for specified currency."""
        symbols = {
            'NPR': 'Rs.',
            'USD': '$',
            'EUR': '€'
        }
        return symbols.get(currency.upper(), 'Rs.')
    
    def get_primary_image(self):
        """Get the primary gallery image or fall back to main image."""
        primary = self.gallery_images.filter(is_primary=True).first()
        if primary:
            return primary.image
        return self.image
    
    def get_gallery_images(self):
        """Get all gallery images for this room ordered by display order."""
        return self.gallery_images.all().order_by('order', '-uploaded_at')


class RoomImage(models.Model):
    """
    Model for room gallery images - multiple images per room.
    
    Fields:
        room (ForeignKey): The room this image belongs to.
        image (ImageField): The room photo.
        caption (str): Optional description of the image.
        is_primary (bool): Whether this is the main image for the room.
        order (int): Display order in the gallery.
        uploaded_at (DateTime): When the image was uploaded.
    """
    
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        help_text="The room this image belongs to"
    )
    image = models.ImageField(
        upload_to='rooms/gallery/',
        help_text="Room gallery photo"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional description (e.g., 'Main Bedroom', 'Bathroom', 'Living Area')"
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Set as the main image for this room"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order in gallery (lower numbers first)"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-uploaded_at']
        verbose_name = 'Room Image'
        verbose_name_plural = 'Room Images'
        unique_together = []
    
    def __str__(self):
        """Return room name and image caption."""
        caption_text = f" - {self.caption}" if self.caption else ""
        return f"{self.room.title}{caption_text}"
    
    def save(self, *args, **kwargs):
        """Ensure only one primary image per room."""
        if self.is_primary:
            # Set all other images for this room to non-primary
            RoomImage.objects.filter(room=self.room, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


class GalleryImage(models.Model):
    """
    Model for gallery images showcasing the resort.
    
    Fields:
        caption (str): Description of the image.
        image (ImageField): The gallery photo.
        upload_date (DateTime): When the image was uploaded.
    """
    
    caption = models.CharField(
        max_length=200,
        help_text="Short description of the gallery image"
    )
    image = models.ImageField(
        upload_to='gallery/',
        help_text="Gallery photo"
    )
    upload_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-upload_date']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
    
    def __str__(self):
        """Return image caption."""
        return self.caption


class BlogPost(models.Model):
    """
    Model for blog posts with SEO optimization.
    
    Fields:
        title (str): Title of the blog post.
        slug (str): URL-friendly identifier, auto-populated from title.
        content (TextField): Full content of the blog post.
        excerpt (TextField): Short summary/teaser of the post.
        image (ImageField): Featured image for the blog post.
        author (str): Name of the blog author.
        created_at (DateTime): When the post was published.
        updated_at (DateTime): When the post was last updated.
        is_published (bool): Whether the post is published.
        meta_title (str): SEO title (for search results).
        meta_description (str): SEO description (for search results).
        meta_keywords (str): SEO keywords (comma-separated).
    """
    
    title = models.CharField(
        max_length=200,
        unique=True,
        help_text="Blog post title"
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        help_text="Auto-generated URL slug"
    )
    excerpt = models.TextField(
        help_text="Short summary of the blog post (appears in listings)"
    )
    content = models.TextField(
        help_text="Full content of the blog post"
    )
    image = models.ImageField(
        upload_to='blog/',
        help_text="Featured image for the blog post"
    )
    author = models.CharField(
        max_length=100,
        default='Diamond Hill Resort',
        help_text="Author name"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(
        default=True,
        help_text="Whether this post is published"
    )
    
    # SEO Fields
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        help_text="SEO Title (50-60 chars). Leave empty to use post title."
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="SEO Description (150-160 chars). Leave empty to use excerpt."
    )
    meta_keywords = models.CharField(
        max_length=200,
        blank=True,
        help_text="SEO Keywords (comma-separated). Example: Nagarkot, Nepal, Resort, Hiking"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        """Return blog post title."""
        return self.title
    
    def save(self, *args, **kwargs):
        """Auto-populate slug from title if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Return the URL for viewing this blog post."""
        return reverse('main:blog_detail', kwargs={'slug': self.slug})
    
    def get_meta_title(self):
        """Get SEO title with fallback to post title."""
        return self.meta_title if self.meta_title else self.title
    
    def get_meta_description(self):
        """Get SEO description with fallback to excerpt."""
        return self.meta_description if self.meta_description else self.excerpt[:160]
    
    def get_meta_keywords(self):
        """Get SEO keywords."""
        return self.meta_keywords if self.meta_keywords else "Diamond Hill Resort, Nagarkot, Nepal, Travel, Blog"
    
    def get_reading_time(self):
        """Calculate approximate reading time in minutes."""
        word_count = len(self.content.split())
        reading_time = max(1, word_count // 200)
        return reading_time


class RoomInventory(models.Model):
    """
    Model to track room inventory (number of available rooms per type).
    
    Fields:
        room (ForeignKey): Reference to the Room model.
        total_rooms (int): Total number of rooms of this type.
        available_rooms (int): Current number of available rooms.
        updated_at (DateTime): Last update timestamp.
    """
    
    room = models.OneToOneField(
        Room,
        on_delete=models.CASCADE,
        related_name='inventory',
        help_text="Room type"
    )
    total_rooms = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Total number of rooms of this type"
    )
    available_rooms = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)],
        help_text="Currently available rooms (auto-calculated)"
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Room Inventory'
        verbose_name_plural = 'Room Inventory'
    
    def __str__(self):
        """Return inventory summary."""
        return f"{self.room.title} - {self.available_rooms}/{self.total_rooms} available"
    
    def save(self, *args, **kwargs):
        """Ensure available_rooms doesn't exceed total_rooms."""
        if self.available_rooms > self.total_rooms:
            self.available_rooms = self.total_rooms
        super().save(*args, **kwargs)
    
    def get_booked_rooms(self, check_in, check_out):
        """Get number of rooms booked for a specific date range."""
        from django.db.models import Count
        from django.db.models import Q
        
        bookings = Booking.objects.filter(
            room=self.room,
            payment_status__in=['paid', 'confirmed'],
            check_in__lt=check_out,
            check_out__gt=check_in
        ).count()
        return bookings
    
    def get_available_count(self, check_in, check_out):
        """Get available room count for a specific date range."""
        booked = self.get_booked_rooms(check_in, check_out)
        return max(0, self.total_rooms - booked)
    
    def is_available(self, check_in, check_out, rooms_needed=1):
        """Check if enough rooms are available for the date range."""
        available = self.get_available_count(check_in, check_out)
        return available >= rooms_needed


class Booking(models.Model):
    """
    Model representing a guest booking.
    
    Fields:
        guest_name (str): Full name of the guest.
        guest_email (str): Email address of the guest.
        guest_phone (str): Phone number of the guest.
        room (ForeignKey): Reference to the Room model.
        check_in (Date): Check-in date.
        check_out (Date): Check-out date.
        guests (int): Number of guests.
        total_amount (Decimal): Total booking cost in NPR.
        currency (str): Currency code (default: 'NPR').
        payment_status (str): Current payment status.
        created_at (DateTime): Booking creation timestamp.
        updated_at (DateTime): Last update timestamp.
    """
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('confirmed', 'Confirmed'),
    ]
    
    guest_name = models.CharField(
        max_length=100,
        help_text="Full name of the guest"
    )
    guest_email = models.EmailField(
        validators=[EmailValidator()],
        help_text="Email address of the guest"
    )
    guest_phone = models.CharField(
        max_length=20,
        help_text="Phone number of the guest"
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text="Room type being booked"
    )
    check_in = models.DateField(
        help_text="Check-in date"
    )
    check_out = models.DateField(
        help_text="Check-out date"
    )
    guests = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of guests"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Total booking amount in NPR"
    )
    currency = models.CharField(
        max_length=3,
        default='NPR',
        help_text="Currency code"
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        help_text="Current payment status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
    
    def __str__(self):
        """Return booking summary."""
        return f"{self.guest_name} - {self.room.title} ({self.check_in})"
    
    def get_number_of_nights(self):
        """Calculate the number of nights for this booking."""
        if self.check_in and self.check_out:
            return (self.check_out - self.check_in).days
        return 0
    
    def get_absolute_url(self):
        """Return the URL for booking details (if needed)."""
        return reverse('main:booking_list')


class HeroSection(models.Model):
    """
    Model for managing hero section slides with images and text.
    
    Fields:
        title (str): Hero slide title.
        subtitle (str): Hero slide subtitle.
        description (str): Hero slide description text.
        image (ImageField): Hero slide background image.
        order (int): Display order (1-6).
        is_active (bool): Whether this slide is displayed.
        created_at (DateTime): When the slide was created.
        updated_at (DateTime): When the slide was last updated.
    """
    
    title = models.CharField(
        max_length=100,
        help_text="Hero slide title"
    )
    subtitle = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional subtitle (e.g., 'Blessed by Nature')"
    )
    description = models.TextField(
        help_text="Main description text for the hero slide"
    )
    image = models.ImageField(
        upload_to='hero/',
        help_text="Background image for the hero slide"
    )
    order = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), ],
        help_text="Display order (1-6)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this slide is displayed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Sections'
        unique_together = ('order',)
    
    def __str__(self):
        """Return hero slide title."""
        return f"{self.title} (Order: {self.order})"
    
    def save(self, *args, **kwargs):
        """Ensure only up to 6 slides are allowed."""
        if self.pk is None:  # Only check on creation
            count = HeroSection.objects.count()
            if count >= 6:
                raise ValueError("Maximum 6 hero slides allowed")
        super().save(*args, **kwargs)


class Review(models.Model):
    """
    Model for managing guest reviews.
    
    Fields:
        guest_name (str): Name of the guest who left the review.
        location (str): City and country of the guest.
        rating (int): Star rating (1-5).
        review_text (str): Full review content.
        is_published (bool): Whether the review is displayed on the site.
        created_at (DateTime): When the review was created.
        updated_at (DateTime): When the review was last updated.
    """
    
    RATING_CHOICES = [
        (1, '⭐ 1 Star'),
        (2, '⭐⭐ 2 Stars'),
        (3, '⭐⭐⭐ 3 Stars'),
        (4, '⭐⭐⭐⭐ 4 Stars'),
        (5, '⭐⭐⭐⭐⭐ 5 Stars'),
    ]
    
    guest_name = models.CharField(
        max_length=100,
        help_text="Name of the guest"
    )
    location = models.CharField(
        max_length=150,
        help_text="City and country (e.g., 'London, UK')"
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        help_text="Star rating from 1-5"
    )
    review_text = models.TextField(
        help_text="The review content"
    )
    visited_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when the guest visited the resort"
    )
    is_published = models.BooleanField(
        default=False,
        help_text="Whether this review is displayed on the site"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
    
    def __str__(self):
        """Return review summary."""
        return f"{self.guest_name} - {self.get_rating_display()}"
    
    def get_stars_display(self):
        """Return star count for displaying in templates."""
        return self.rating


class About(models.Model):
    """
    Model for managing the About page content.
    This is a singleton model - only one instance should exist.
    
    Fields:
        title (str): Page title
        story (str): Main "Our Story" section content
        values_intro (str): Introduction text for values section
        image (ImageField): Featured image for about section (homepage)
        updated_at (DateTime): When the content was last updated
    """
    
    title = models.CharField(
        max_length=200,
        default='About Diamond Hill Resort',
        help_text="About page title"
    )
    story = models.TextField(
        help_text="Main story and background content for the About page",
        default="Diamond Hill Resort stands as a beacon of luxury and comfort in the heart of Nagarkot, Nepal..."
    )
    values_intro = models.TextField(
        blank=True,
        help_text="Introduction text before the values section"
    )
    image = models.ImageField(
        upload_to='about/',
        blank=True,
        null=True,
        help_text="Featured image for about section on homepage"
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'About Page'
        verbose_name_plural = 'About Page'
    
    def __str__(self):
        """Return title."""
        return self.title
    
    def save(self, *args, **kwargs):
        """Ensure only one About instance exists (singleton pattern)."""
        if not self.pk and About.objects.exists():
            # If creating a new instance, delete the old one
            About.objects.all().delete()
        super().save(*args, **kwargs)

