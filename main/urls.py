"""
URL configuration for the main app.

Namespace: 'main'

URL Patterns:
- /: Home page
- /rooms/: Room listing
- /rooms/<slug>/: Room detail
- /gallery/: Gallery page
- /booking/: Booking form
- /booking/success/: Booking success
- /contact/: Contact page
- /payment/checkout/: Payment checkout page
- /payment/stripe/: Stripe payment processing
- /payment/khalti/: Khalti payment processing
- /payment/khalti/verify/: Khalti payment verification
- /payment/callback/<gateway>/: Payment webhook endpoint
"""

from django.urls import path
from . import views
from .cloudinary_test import test_cloudinary

app_name = 'main'

urlpatterns = [
    # Home page
    path('', views.HomeView.as_view(), name='home'),
    
    # Rooms
    path('rooms/', views.RoomListView.as_view(), name='room_list'),
    path('rooms/<slug:slug>/', views.RoomDetailView.as_view(), name='room_detail'),
    
    # Gallery
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    
    # Blog
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    
    # Booking
    path('booking/', views.BookingCreateView.as_view(), name='booking'),
    path('booking/success/', views.BookingSuccessView.as_view(), name='booking_success'),
    path('api/check-availability/', views.CheckAvailabilityView.as_view(), name='check_availability'),
    
    # Contact
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # About
    path('about/', views.AboutView.as_view(), name='about'),
    
    # Payment
    path('payment/checkout/', views.PaymentCheckoutView.as_view(), name='payment_checkout'),
    path('payment/stripe/', views.StripePaymentView.as_view(), name='stripe_payment'),
    path('payment/khalti/', views.KhaltiPaymentView.as_view(), name='khalti_payment'),
    path('payment/khalti/verify/', views.KhaltiVerifyView.as_view(), name='khalti_verify'),
    path('payment/webhook/stripe/', views.StripeWebhookView.as_view(), name='stripe_webhook'),
    
    # Payment callbacks (legacy)
    path('payment/callback/<str:gateway>/', views.PaymentCallbackView.as_view(), name='payment_callback'),
    
    # Debug endpoints (only in DEBUG mode)
    path('debug/test-cloudinary/', test_cloudinary, name='test_cloudinary'),
]
