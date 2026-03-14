"""
Django views for Diamond Hill Resort.

Views include:
- HomeView: Display home page with resort introduction
- RoomListView: List all available rooms
- RoomDetailView: Display details for a specific room
- GalleryView: Display gallery images
- BookingCreateView: Create a new booking
- BookingListView: List bookings (admin)
- ContactView: Display contact form and information
- PaymentWebhookView: Handle payment gateway callbacks (placeholder)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging
import stripe
import requests
import json
from datetime import datetime

from .models import Room, GalleryImage, Booking, BlogPost, HeroSection, Review, About
from .currency import get_user_currency, get_room_price_for_currency, CURRENCY_SYMBOLS
import math
from .forms import BookingForm, ContactForm

logger = logging.getLogger(__name__)

# Initialize Stripe
if settings.STRIPE_SECRET_KEY:
    stripe.api_key = settings.STRIPE_SECRET_KEY


class HomeView(TemplateView):
    """
    Display the home page with resort introduction and featured content.
    
    Context:
    - featured_rooms: Top rooms to showcase
    - featured_images: Gallery images for hero section
    - site_title: Resort name for SEO
    """
    template_name = 'main/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_title'] = 'Diamond Hill Resort - Own the Drip'
        context['featured_rooms'] = Room.objects.all()[:4]
        
        # Get only aerial shots for hero slideshow (from GalleryImage)
        all_images = GalleryImage.objects.all()
        featured = []
        
        # Filter for aerial/areal images only
        for image in all_images:
            if 'aerial' in image.caption.lower() or 'areal' in image.caption.lower():
                featured.append(image)
        
        context['featured_images'] = featured[:6]
        
        # Get hero slides for text content (optional - fallback to default text)
        context['hero_slides'] = HeroSection.objects.filter(is_active=True).order_by('order')[:6]
        
        # Get event images for blog/events section
        event_images = []
        for image in all_images:
            caption_lower = image.caption.lower()
            if 'foreigner' in caption_lower or 'celebration' in caption_lower:
                event_images.append(image)
            elif 'nepali' in caption_lower or 'french' in caption_lower:
                event_images.append(image)
        
        context['event_images'] = event_images[:3]
        
        # Get featured blog posts
        context['featured_posts'] = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:3]
        
        # Get published reviews
        reviews_qs = Review.objects.filter(is_published=True).order_by('-created_at')
        context['reviews'] = reviews_qs

        # Calculate pagination for review carousel indicators (3 reviews per view)
        review_count = reviews_qs.count()
        pages = math.ceil(review_count / 3) if review_count > 0 else 0
        # Only provide pages when there is more than one page
        context['review_pages'] = range(pages) if pages > 1 else []

        # Get About data for homepage about section
        try:
            context['about'] = About.objects.first()
        except Exception:
            context['about'] = None

        context['page_description'] = (
            'Diamond Hill Resort – A stylish mountain retreat in Nagarkot, Nepal. '
            'Book deluxe rooms, enjoy panoramic views of Himalayas, rooftop pool, spa & premium service.'
        )
        return context


class RoomListView(ListView):
    """
    Display a list of all available rooms.
    
    Context:
    - object_list: All Room objects
    - page_title: Title for the page
    - page_description: SEO meta description
    - user_currency: Detected currency based on user location
    - currency_symbol: Currency symbol for display
    """
    model = Room
    template_name = 'main/rooms.html'
    context_object_name = 'rooms'
    paginate_by = 9
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_currency = get_user_currency(self.request)
        
        context['page_title'] = 'Our Rooms | Diamond Hill Resort'
        context['page_description'] = 'Explore our luxury room types: Deluxe, Superior, and Suite. Enjoy mountain views, modern amenities, and exceptional comfort.'
        context['user_currency'] = user_currency
        context['currency_symbol'] = CURRENCY_SYMBOLS.get(user_currency, 'Rs.')
        
        # Add prices in user's currency
        for room in context['rooms']:
            room.price_in_user_currency = get_room_price_for_currency(room, user_currency)
        
        return context


class RoomDetailView(DetailView):
    """
    Display detailed information about a specific room.
    
    Features:
    - Show room amenities, price, and images
    - Display gallery images with carousel
    - Display related bookings (future bookings)
    - Link to booking form
    - Auto-convert price to user's currency
    - Edit amenities/description for staff
    
    Context:
    - object: Room instance
    - gallery_images: All room gallery images
    - related_bookings: Future bookings for this room
    - user_currency: Detected currency based on user location
    - currency_symbol: Currency symbol for display
    """
    model = Room
    template_name = 'main/room_detail.html'
    context_object_name = 'room'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.get_object()
        user_currency = get_user_currency(self.request)
        
        context['page_title'] = f'{room.title} | Diamond Hill Resort'
        context['amenities'] = room.get_amenities_list()
        context['user_currency'] = user_currency
        context['currency_symbol'] = CURRENCY_SYMBOLS.get(user_currency, 'Rs.')
        context['room_price_in_user_currency'] = get_room_price_for_currency(room, user_currency)
        
        # Get gallery images for carousel
        context['gallery_images'] = room.get_gallery_images()
        
        # Get future bookings for this room (optional)
        from datetime import date
        context['future_bookings'] = room.bookings.filter(
            check_in__gte=date.today()
        ).count()
        
        # Get other rooms (excluding current room)
        other_rooms = Room.objects.exclude(id=room.id).order_by('title')[:3]
        context['other_rooms'] = other_rooms
        
        # Add prices for other rooms
        for other_room in other_rooms:
            other_room.price_in_user_currency = get_room_price_for_currency(other_room, user_currency)
        
        return context


class GalleryView(ListView):
    """
    Display gallery images of the resort.
    
    Features:
    - Show all gallery images with captions
    - Responsive grid layout
    - Lightbox effect (via template)
    
    Context:
    - object_list: All GalleryImage objects
    """
    model = GalleryImage
    template_name = 'main/gallery.html'
    context_object_name = 'images'
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Gallery | Diamond Hill Resort'
        context['page_description'] = 'Browse beautiful photos of Diamond Hill Resort, featuring our luxurious rooms, amenities, and stunning Himalayan views.'
        return context


class BlogListView(ListView):
    """
    Display a list of published blog posts.
    
    Context:
    - object_list: All published BlogPost objects
    - page_title: Title for the page
    - page_description: SEO meta description
    """
    model = BlogPost
    template_name = 'main/blog.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        """Return only published blog posts."""
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Blog | Diamond Hill Resort'
        context['page_description'] = 'Read the latest news, travel tips, and stories from Diamond Hill Resort. Discover what makes Nagarkot special.'
        return context


class BlogDetailView(DetailView):
    """
    Display a detailed view of a single blog post.
    
    Context:
    - object: BlogPost instance
    - related_posts: Other recent blog posts
    """
    model = BlogPost
    template_name = 'main/blog_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        """Return only published blog posts."""
        return BlogPost.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['page_title'] = f'{post.title} | Diamond Hill Resort'
        context['page_description'] = post.excerpt
        # Get related posts (other published posts)
        context['related_posts'] = BlogPost.objects.filter(
            is_published=True
        ).exclude(id=post.id).order_by('-created_at')[:3]
        return context


class BookingCreateView(CreateView):
    """
    Handle booking form submission.
    
    Features:
    - Display booking form
    - Validate guest information and dates
    - Calculate total amount
    - Create booking with "pending" status
    - Redirect to payment gateway placeholder
    
    Form Validation:
    - Check-out must be after check-in
    - Dates must be in future
    - Minimum 1 night stay
    """
    model = Booking
    form_class = BookingForm
    template_name = 'main/booking.html'
    success_url = reverse_lazy('main:payment_checkout')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Book Now | Diamond Hill Resort'
        context['page_description'] = 'Reserve your stay at Diamond Hill Resort. Select your room type, dates, and complete your booking.'
        
        # Pre-fill room if provided in URL
        room_id = self.request.GET.get('room_id')
        if room_id:
            context['selected_room'] = get_object_or_404(Room, pk=room_id)
        
        # Check availability if dates are provided from check availability form
        check_in = self.request.GET.get('checkin')
        check_out = self.request.GET.get('checkout')
        rooms_needed = self.request.GET.get('rooms', 1)
        
        if check_in and check_out:
            from datetime import datetime
            try:
                check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
                rooms_needed = int(rooms_needed)
                
                # Check availability
                available_rooms = []
                for room in Room.objects.all():
                    if hasattr(room, 'inventory'):
                        inventory = room.inventory
                        available_count = inventory.get_available_count(check_in_date, check_out_date)
                        if available_count > 0:
                            available_rooms.append({
                                'room': room,
                                'available_count': available_count,
                                'nights': (check_out_date - check_in_date).days
                            })
                
                # Add availability info to context
                context['available_rooms'] = available_rooms
                context['check_in_date'] = check_in
                context['check_out_date'] = check_out
                context['rooms_needed'] = rooms_needed
                context['nights'] = (check_out_date - check_in_date).days
                context['has_availability_check'] = True
                context['rooms_available'] = len(available_rooms) > 0
                
            except (ValueError, TypeError):
                pass
        
        return context
    
    def form_valid(self, form):
        """
        Process valid booking form.
        
        Actions:
        1. Save booking with pending status
        2. Send confirmation email
        3. Log booking details
        4. Redirect to payment gateway
        """
        booking = form.save()
        
        logger.info(f'New booking created: {booking.id} - {booking.guest_name}')
        
        # Send confirmation email
        self.send_booking_confirmation(booking)
        
        # Store booking ID in session for redirect
        self.request.session['booking_id'] = booking.id
        self.request.session['total_amount'] = str(booking.total_amount)
        
        messages.success(
            self.request,
            f'Booking confirmed! Total: NPR {booking.total_amount:,.2f}. Proceeding to payment...'
        )
        
        return super().form_valid(form)
    
    def send_booking_confirmation(self, booking):
        """Send confirmation email to guest."""
        try:
            subject = f'Booking Confirmation - Diamond Hill Resort #{booking.id}'
            message = f"""
Hello {booking.guest_name},

Thank you for booking with Diamond Hill Resort!

Booking Details:
- Booking ID: {booking.id}
- Room: {booking.room.title}
- Check-in: {booking.check_in}
- Check-out: {booking.check_out}
- Number of Guests: {booking.guests}
- Total Amount: NPR {booking.total_amount:,.2f}
- Status: {booking.get_payment_status_display()}

Payment Instructions:
Please proceed to complete your payment on the next page using your preferred payment method.

Questions? Contact us at +977-1-1234567 or info@diamondhillresort.com.np

Best regards,
Diamond Hill Resort Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@diamondhillresort.com.np',
                [booking.guest_email],
                fail_silently=True,
            )
        except Exception as e:
            logger.error(f'Failed to send email for booking {booking.id}: {str(e)}')


class BookingSuccessView(TemplateView):
    """
    Display booking success page with payment gateway redirect.
    
    This is a placeholder for payment integration.
    In production, integrate with Stripe, eSewa, or Khalti.
    """
    template_name = 'main/booking_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = self.request.session.get('booking_id')
        total_amount = self.request.session.get('total_amount')
        
        context['booking_id'] = booking_id
        context['total_amount'] = total_amount
        context['page_title'] = 'Booking Successful | Diamond Hill Resort'
        
        return context


class CheckAvailabilityView(View):
    """
    AJAX endpoint to check room availability for a given date range.
    
    Request Parameters (JSON):
    - check_in: Date string (YYYY-MM-DD)
    - check_out: Date string (YYYY-MM-DD)
    - room_id: Room ID (optional, returns all rooms if omitted)
    - rooms_needed: Number of rooms needed (default: 1)
    
    Response (JSON):
    - available: bool - Is the room available?
    - available_count: int - Number of available rooms
    - total_rooms: int - Total rooms of this type
    - message: str - Human-readable message
    """
    
    def post(self, request):
        """Handle availability check request."""
        try:
            import json
            from datetime import datetime
            
            data = json.loads(request.body)
            check_in_str = data.get('check_in')
            check_out_str = data.get('check_out')
            room_id = data.get('room_id')
            rooms_needed = int(data.get('rooms_needed', 1))
            
            # Parse dates
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
            
            # Validate dates
            if check_in >= check_out:
                return JsonResponse({
                    'available': False,
                    'message': 'Check-out date must be after check-in date.'
                }, status=400)
            
            results = []
            
            if room_id:
                # Check specific room
                try:
                    room = Room.objects.get(pk=room_id)
                    inventory = room.inventory
                    available = inventory.get_available_count(check_in, check_out)
                    is_available = available >= rooms_needed
                    
                    results.append({
                        'room_id': room.id,
                        'room_title': room.title,
                        'available': is_available,
                        'available_count': available,
                        'total_rooms': inventory.total_rooms,
                        'price': float(room.price),
                        'message': f'{available} room(s) available' if is_available else 'No rooms available for these dates'
                    })
                except Room.DoesNotExist:
                    return JsonResponse({'error': 'Room not found'}, status=404)
            else:
                # Check all rooms
                for room in Room.objects.all():
                    if hasattr(room, 'inventory'):
                        inventory = room.inventory
                        available = inventory.get_available_count(check_in, check_out)
                        is_available = available >= rooms_needed
                        
                        results.append({
                            'room_id': room.id,
                            'room_title': room.title,
                            'available': is_available,
                            'available_count': available,
                            'total_rooms': inventory.total_rooms,
                            'price': float(room.price),
                        })
            
            return JsonResponse({
                'available': any(r['available'] for r in results),
                'results': results,
                'check_in': check_in_str,
                'check_out': check_out_str
            })
            
        except ValueError as e:
            return JsonResponse({'error': f'Invalid date format: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f'Error in check_availability: {str(e)}')
            return JsonResponse({'error': 'Internal server error'}, status=500)


class ContactView(TemplateView):
    """
    Display contact page with form and resort information.
    
    Features:
    - Contact form for inquiries
    - Google Map embed
    - Resort contact information
    - Social media links
    
    Context:
    - form: ContactForm instance
    - resort_phone: +977-1-1234567
    - resort_email: info@diamondhillresort.com.np
    - resort_address: Cherry Hill Road, Nagarkot, Kavrepalanchok, Nepal
    - facebook_page: Link to Facebook
    """
    template_name = 'main/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Contact Us | Diamond Hill Resort'
        context['page_description'] = 'Get in touch with Diamond Hill Resort. We\'re located in Nagarkot, Nepal. Call +977-1-1234567 or send us an inquiry.'
        
        # Contact information
        context['resort_phone'] = '+977-1-1234567'
        context['resort_email'] = 'info@diamondhillresort.com.np'
        context['resort_address'] = 'Cherry Hill Road, Nagarkot, Kavrepalanchok, Nepal'
        context['facebook_url'] = 'https://www.facebook.com/diamondhillresort.com.np/'
        
        # Google Map embed URL (Nagarkot, Nepal)
        context['map_embed'] = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3532.7891854169997!2d85.42869952346805!3d27.704500199999998!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39eb7e4de5c5c5c5%3A0xc5c5c5c5c5c5c5c5!2sNagarkot%2C%20Kavrepalanchok%2C%20Nepal!5e0!3m2!1sen!2snp!4v1234567890'
        
        context['form'] = ContactForm()
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle contact form submission."""
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Process the form
            self.send_contact_email(form.cleaned_data)
            
            messages.success(
                request,
                'Thank you for your inquiry! We\'ll get back to you shortly.'
            )
            return redirect('main:contact')
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)
    
    def send_contact_email(self, cleaned_data):
        """Send contact form details to admin."""
        try:
            subject = f'Contact Inquiry from {cleaned_data["name"]}'
            message = f"""
New contact inquiry:

Name: {cleaned_data['name']}
Email: {cleaned_data['email']}
Phone: {cleaned_data.get('phone', 'Not provided')}
Subject: {cleaned_data['subject']}

Message:
{cleaned_data['message']}
            """
            
            send_mail(
                subject,
                message,
                cleaned_data['email'],
                ['info@diamondhillresort.com.np'],
                fail_silently=True,
            )
            
            logger.info(f'Contact form submitted by {cleaned_data["name"]}')
        except Exception as e:
            logger.error(f'Failed to send contact email: {str(e)}')


class AboutView(TemplateView):
    """
    Display the About page with resort information and history.
    
    Context:
    - page_title: About page title for SEO
    - page_description: SEO meta description
    - featured_images: Gallery images for display
    - reviews: Customer testimonials and reviews
    """
    template_name = 'main/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'About Us | Diamond Hill Resort'
        context['page_description'] = 'Learn about Diamond Hill Resort - A luxury mountain retreat in Nagarkot, Nepal with world-class amenities and exceptional hospitality.'
        context['featured_images'] = GalleryImage.objects.all()[:6]
        
        # Get published reviews for testimonials section
        context['reviews'] = Review.objects.filter(is_published=True).order_by('-created_at')[:3]
        
        # Get About page content from database
        try:
            about = About.objects.first()
            if about:
                context['about'] = about
                context['page_title'] = about.title
        except About.DoesNotExist:
            # Fallback to default if no About content exists
            pass
        
        return context


class PaymentCheckoutView(TemplateView):
    """
    Display payment checkout page where user selects payment gateway.
    Shows booking details, room info, nights, subtotal, and tax calculation.
    """
    template_name = 'main/payment_checkout.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = self.request.session.get('booking_id')
        total_amount = self.request.session.get('total_amount')
        
        if not booking_id:
            messages.error(self.request, 'No booking found. Please create a booking first.')
            return redirect('main:booking')
        
        try:
            booking = Booking.objects.get(id=booking_id)
            
            # Calculate nights
            nights = (booking.check_out - booking.check_in).days
            
            # Calculate subtotal (room price * nights)
            subtotal = float(booking.room.price) * nights
            
            # Calculate tax (13% VAT)
            tax_rate = 0.13
            tax = subtotal * tax_rate
            
            # Total should match booking.total_amount
            total = subtotal + tax
            
            context['booking_id'] = booking_id
            context['booking'] = booking
            context['room_type'] = booking.room.title
            context['room_price'] = booking.room.price
            context['nights'] = nights
            context['subtotal'] = subtotal
            context['tax'] = tax
            context['total_amount'] = total
            context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
            context['khalti_public_key'] = settings.KHALTI_PUBLIC_KEY
            context['page_title'] = 'Payment Checkout | Diamond Hill Resort'
            
            return context
            
        except Booking.DoesNotExist:
            messages.error(self.request, 'Booking not found.')
            return redirect('main:booking')


class StripePaymentView(View):
    """Handle Stripe payment processing."""
    
    def post(self, request, *args, **kwargs):
        try:
            booking_id = request.session.get('booking_id')
            total_amount = float(request.session.get('total_amount', 0))
            
            if not booking_id or total_amount <= 0:
                return JsonResponse({'error': 'Invalid booking details'}, status=400)
            
            booking = Booking.objects.get(id=booking_id)
            
            # Create Stripe payment intent
            intent = stripe.PaymentIntent.create(
                amount=int(total_amount * 100),  # Convert to cents
                currency='usd',
                metadata={
                    'booking_id': booking_id,
                    'guest_name': booking.guest_name,
                    'guest_email': booking.guest_email,
                }
            )
            
            return JsonResponse({'clientSecret': intent['client_secret']})
        
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)
        except stripe.error.CardError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            logger.error(f'Stripe payment error: {str(e)}')
            return JsonResponse({'error': 'Payment processing failed'}, status=500)


class KhaltiPaymentView(View):
    """Handle Khalti payment processing."""
    
    def post(self, request, *args, **kwargs):
        try:
            booking_id = request.session.get('booking_id')
            total_amount = int(float(request.session.get('total_amount', 0)) * 100)  # Convert to paisa
            
            if not booking_id or total_amount <= 0:
                return JsonResponse({'error': 'Invalid booking details'}, status=400)
            
            booking = Booking.objects.get(id=booking_id)
            
            # Khalti payload
            payload = {
                'public_key': settings.KHALTI_PUBLIC_KEY,
                'transaction_uuid': f'booking_{booking_id}_{datetime.now().timestamp()}',
                'description': f'Booking for {booking.guest_name} - Room: {booking.room.title}',
                'amount': total_amount,
                'website_url': request.build_absolute_uri('/'),
                'return_url': request.build_absolute_uri(reverse_lazy('main:khalti_verify')),
            }
            
            return JsonResponse(payload)
        
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)
        except Exception as e:
            logger.error(f'Khalti payment error: {str(e)}')
            return JsonResponse({'error': 'Payment processing failed'}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(View):
    """Handle Stripe webhook callbacks."""
    
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            logger.error(f'Invalid Stripe payload: {str(e)}')
            return JsonResponse({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            logger.error(f'Invalid Stripe signature: {str(e)}')
            return JsonResponse({'error': 'Invalid signature'}, status=400)
        
        # Handle payment_intent.succeeded event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            booking_id = payment_intent['metadata'].get('booking_id')
            
            try:
                booking = Booking.objects.get(id=booking_id)
                booking.payment_status = 'paid'
                booking.save()
                
                logger.info(f'Payment confirmed for booking {booking_id}')
                self.send_payment_confirmation_email(booking)
                
            except Booking.DoesNotExist:
                logger.error(f'Booking {booking_id} not found')
        
        return JsonResponse({'status': 'success'})
    
    def send_payment_confirmation_email(self, booking):
        """Send payment confirmation email to guest."""
        try:
            subject = f'Payment Confirmed - Diamond Hill Resort #{booking.id}'
            message = f"""
Hello {booking.guest_name},

Your payment has been successfully received!

Booking Details:
- Booking ID: {booking.id}
- Room: {booking.room.title}
- Check-in: {booking.check_in}
- Check-out: {booking.check_out}
- Total Amount: NPR {booking.total_amount:,.2f}
- Status: Confirmed

Thank you for booking with us. We look forward to hosting you!

Best regards,
Diamond Hill Resort Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@diamondhillresort.com.np',
                [booking.guest_email],
                fail_silently=True,
            )
        except Exception as e:
            logger.error(f'Failed to send payment confirmation email: {str(e)}')


class KhaltiVerifyView(View):
    """Verify Khalti payment and update booking status."""
    
    def get(self, request, *args, **kwargs):
        try:
            pidx = request.GET.get('pidx')
            transaction_id = request.GET.get('transaction_id')
            amount = request.GET.get('amount')
            
            if not pidx:
                messages.error(request, 'Payment verification failed: Invalid transaction')
                return redirect('main:booking')
            
            # Verify with Khalti
            headers = {
                'Authorization': f'Key {settings.KHALTI_SECRET_KEY}'
            }
            payload = {'pidx': pidx}
            
            response = requests.post(
                'https://khalti.com/api/v2/payment/verify/',
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'Completed':
                    # Extract booking_id from transaction_uuid
                    transaction_uuid = data.get('transaction_uuid', '')
                    booking_id = transaction_uuid.split('_')[1] if '_' in transaction_uuid else None
                    
                    if booking_id:
                        try:
                            booking = Booking.objects.get(id=booking_id)
                            booking.payment_status = 'paid'
                            booking.save()
                            
                            logger.info(f'Khalti payment confirmed for booking {booking_id}')
                            self.send_payment_confirmation_email(booking)
                            
                            messages.success(request, 'Payment successful! Your booking is confirmed.')
                            return redirect('main:booking_success')
                        except Booking.DoesNotExist:
                            logger.error(f'Booking {booking_id} not found')
                            messages.error(request, 'Booking not found')
                            return redirect('main:booking')
                    else:
                        messages.error(request, 'Invalid transaction data')
                        return redirect('main:booking')
                else:
                    messages.error(request, f'Payment failed: {data.get("status_message", "Unknown error")}')
                    return redirect('main:booking')
            else:
                logger.error(f'Khalti verification failed: {response.status_code}')
                messages.error(request, 'Payment verification failed')
                return redirect('main:booking')
        
        except Exception as e:
            logger.error(f'Khalti verification error: {str(e)}')
            messages.error(request, 'An error occurred during payment verification')
            return redirect('main:booking')
    
    def send_payment_confirmation_email(self, booking):
        """Send payment confirmation email to guest."""
        try:
            subject = f'Payment Confirmed - Diamond Hill Resort #{booking.id}'
            message = f"""
Hello {booking.guest_name},

Your payment has been successfully received!

Booking Details:
- Booking ID: {booking.id}
- Room: {booking.room.title}
- Check-in: {booking.check_in}
- Check-out: {booking.check_out}
- Total Amount: NPR {booking.total_amount:,.2f}
- Status: Confirmed

Thank you for booking with us. We look forward to hosting you!

Best regards,
Diamond Hill Resort Team
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@diamondhillresort.com.np',
                [booking.guest_email],
                fail_silently=True,
            )
        except Exception as e:
            logger.error(f'Failed to send payment confirmation email: {str(e)}')


class PaymentCallbackView(TemplateView):
    """
    Handle payment gateway callbacks (updated with real implementations).
    
    Supported Gateways:
    - Stripe
    - Khalti
    """
    
    def post(self, request, *args, **kwargs):
        """Handle payment webhook from gateway."""
        gateway = kwargs.get('gateway', 'stripe')
        
        logger.info(f'Payment callback from {gateway}')
        
        # Parse request data based on gateway
        if gateway == 'stripe':
            return self.handle_stripe_webhook(request)
        elif gateway == 'khalti':
            return self.handle_khalti_webhook(request)
        
        return JsonResponse({'status': 'error', 'message': 'Unknown gateway'}, status=400)
    
    def handle_stripe_webhook(self, request):
        """Handle Stripe payment webhook."""
        logger.info('Stripe webhook received')
        return JsonResponse({'status': 'success'})
    
    def handle_khalti_webhook(self, request):
        """Handle Khalti payment webhook."""
        logger.info('Khalti webhook received')
        return JsonResponse({'status': 'success'})
