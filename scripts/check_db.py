#!/usr/bin/env python
"""Check database content for testing."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resort_website.settings')
django.setup()

from main.models import Room, GalleryImage, BlogPost, HeroSection, Review, About, Booking

print("=" * 50)
print("DATABASE CONTENT CHECK")
print("=" * 50)
print(f"Rooms: {Room.objects.count()}")
print(f"Gallery Images: {GalleryImage.objects.count()}")
print(f"Blog Posts (Published): {BlogPost.objects.filter(is_published=True).count()}")
print(f"Blog Posts (All): {BlogPost.objects.count()}")
print(f"Hero Sections (Active): {HeroSection.objects.filter(is_active=True).count()}")
print(f"Hero Sections (All): {HeroSection.objects.count()}")
print(f"Reviews (Published): {Review.objects.filter(is_published=True).count()}")
print(f"Reviews (All): {Review.objects.count()}")
print(f"About Entries: {About.objects.count()}")
print(f"Bookings: {Booking.objects.count()}")

print("\n" + "=" * 50)
print("SAMPLE DATA")
print("=" * 50)

if Room.objects.exists():
    room = Room.objects.first()
    print(f"✓ Sample Room: {room.title} (NPR {room.price})")
else:
    print("✗ No rooms found")

if BlogPost.objects.exists():
    post = BlogPost.objects.first()
    print(f"✓ Sample Blog: {post.title} (Published: {post.is_published})")
else:
    print("✗ No blog posts found")

if HeroSection.objects.exists():
    hero = HeroSection.objects.first()
    print(f"✓ Sample Hero Slide: {hero.title} (Active: {hero.is_active})")
else:
    print("✗ No hero sections found")

if GalleryImage.objects.exists():
    image = GalleryImage.objects.first()
    print(f"✓ Sample Gallery Image: {image.caption}")
else:
    print("✗ No gallery images found")

if Review.objects.exists():
    review = Review.objects.first()
    print(f"✓ Sample Review: {review.rating}★ (Published: {review.is_published})")
else:
    print("✗ No reviews found")

if About.objects.exists():
    about = About.objects.first()
    print(f"✓ About Page: {about.title}")
else:
    print("✗ About page not created")

print("\n" + "=" * 50)
