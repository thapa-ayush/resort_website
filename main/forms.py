"""
Django forms for Diamond Hill Resort.

Forms:
- BookingForm: Form for guest bookings with date validation and total amount calculation.
- ContactForm: Form for contact inquiries.
- BlogPostForm: Form for blog post creation/editing with rich text editor.
"""

from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import Booking, Room, BlogPost
from tinymce.widgets import TinyMCE


class BookingForm(forms.ModelForm):
    """
    Form for creating and updating bookings.
    
    Handles:
    - Guest information (name, email, phone)
    - Booking dates with validation (check_out > check_in, dates in future)
    - Number of guests
    - Automatic total amount calculation
    - Room availability validation
    """
    
    # Additional fields for room selection
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'roomSelect',
            'required': True,
        }),
        help_text='Select the room type you wish to book'
    )
    
    # Number of rooms to book (useful for group bookings)
    num_rooms = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'numRooms',
            'value': 1,
            'min': 1,
            'max': 10,
        }),
        label='Number of Rooms',
        help_text='How many rooms do you need?',
        required=False,
    )
    
    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_email', 'guest_phone', 'room', 'check_in', 'check_out', 'guests']
        widgets = {
            'guest_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'maxlength': 100,
            }),
            'guest_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
            }),
            'guest_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number (e.g., +977-1-1234567)',
                'maxlength': 20,
            }),
            'check_in': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': str(date.today()),
            }),
            'check_out': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': str(date.today() + timedelta(days=1)),
            }),
            'guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'min': 1,
                'max': 10,
                'value': 1,
            }),
        }
        labels = {
            'guest_name': 'Full Name',
            'guest_email': 'Email Address',
            'guest_phone': 'Phone Number',
            'room': 'Room Type',
            'check_in': 'Check-in Date',
            'check_out': 'Check-out Date',
            'guests': 'Number of Guests',
        }
        help_texts = {
            'guest_name': 'Your full name as it should appear in the reservation',
            'guest_email': 'We\'ll use this to send booking confirmation',
            'guest_phone': 'Contact number for the resort to reach you',
            'room': 'Select the room type you prefer',
            'check_in': 'Date of arrival',
            'check_out': 'Date of departure',
            'guests': 'Total number of guests staying',
        }
    
    def clean(self):
        """
        Validate form data:
        - Check-out date must be after check-in date
        - Check-in date must be in the future
        - At least 1 night minimum
        - Check room availability for the selected dates
        """
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        room = cleaned_data.get('room')
        num_rooms = cleaned_data.get('num_rooms') or 1
        
        # Validate check-in date is not in the past
        if check_in and check_in < date.today():
            raise ValidationError(
                'Check-in date cannot be in the past. Please select a future date.'
            )
        
        # Validate check-out date is after check-in date
        if check_in and check_out:
            if check_out <= check_in:
                raise ValidationError(
                    'Check-out date must be after check-in date.'
                )
            
            # Ensure minimum 1 night stay
            nights = (check_out - check_in).days
            if nights < 1:
                raise ValidationError(
                    'Minimum stay is 1 night. Please adjust your dates.'
                )
            
            # Check room availability
            if room and hasattr(room, 'inventory'):
                inventory = room.inventory
                available = inventory.get_available_count(check_in, check_out)
                
                if available < num_rooms:
                    raise ValidationError(
                        f'Only {available} {room.title}(s) available for these dates. '
                        f'You requested {num_rooms}. Please select different dates or reduce the number of rooms.'
                    )
        
        return cleaned_data
    
    def save(self, commit=True):
        """
        Save the booking and calculate the total amount.
        
        Total amount = Room Price × Number of Nights × Number of Guests
        """
        booking = super().save(commit=False)
        num_rooms = self.cleaned_data.get('num_rooms') or 1
        
        # Calculate total amount
        if booking.room and booking.check_in and booking.check_out and booking.guests:
            nights = (booking.check_out - booking.check_in).days
            # Include number of rooms in calculation
            booking.total_amount = booking.room.price * nights * booking.guests * num_rooms
            booking.currency = 'NPR'
            booking.payment_status = 'pending'
        
        if commit:
            booking.save()
        
        return booking


class ContactForm(forms.Form):
    """
    Form for contact inquiries.
    
    Fields:
    - Name: Guest name
    - Email: Guest email address
    - Phone: Contact phone number
    - Subject: Inquiry subject
    - Message: Detailed message
    """
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name',
        }),
        label='Full Name',
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
        }),
        label='Email Address',
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+977-1-1234567',
        }),
        label='Phone Number (Optional)',
    )
    
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject of your inquiry',
        }),
        label='Subject',
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Please describe your inquiry in detail...',
            'rows': 6,
        }),
        label='Message',
    )
    
    def clean_email(self):
        """Validate email format."""
        email = self.cleaned_data.get('email')
        if email:
            # Additional email validation can be added here if needed
            pass
        return email


class BlogPostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts with rich text editor.
    
    Features:
    - TinyMCE editor for content formatting (bold, italic, headings, lists, etc.)
    - SEO fields for meta title, description, and keywords
    - Auto-generated slug from title
    """
    
    class Meta:
        model = BlogPost
        fields = ('title', 'excerpt', 'content', 'image', 'author', 'is_published', 
                  'meta_title', 'meta_description', 'meta_keywords')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter blog post title',
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Short summary for blog listings (50-160 chars)',
                'rows': 3,
            }),
            'content': TinyMCE(attrs={
                'class': 'tinymce',
                'data-theme': 'light',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Diamond Hill Resort',
                'value': 'Diamond Hill Resort',
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SEO title (50-60 chars)',
                'maxlength': 60,
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'SEO description (150-160 chars)',
                'rows': 2,
                'maxlength': 160,
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Comma-separated keywords',
            }),
        }
    
    def clean_title(self):
        """Validate title is not empty."""
        title = self.cleaned_data.get('title')
        if not title or len(title.strip()) < 3:
            raise ValidationError('Title must be at least 3 characters long.')
        return title
    
    def clean_excerpt(self):
        """Validate excerpt length."""
        excerpt = self.cleaned_data.get('excerpt')
        if excerpt and len(excerpt) > 300:
            raise ValidationError('Excerpt must be less than 300 characters.')
        return excerpt
    
    def clean_content(self):
        """Validate content is not empty."""
        content = self.cleaned_data.get('content')
        if not content or len(content.strip()) < 50:
            raise ValidationError('Content must be at least 50 characters long.')
        return content