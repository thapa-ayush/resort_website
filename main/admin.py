"""Django Admin configuration for Diamond Hill Resort."""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import Room, RoomImage, RoomInventory, GalleryImage, Booking, BlogPost, HeroSection, Review, About
from .forms import BlogPostForm

class DiamondHillAdminSite(AdminSite):
    site_header = "🏨 Diamond Hill Resort Admin Dashboard"
    site_title = "Diamond Hill Resort"
    index_title = "Admin Dashboard"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.site_url = None
        
    def each_context(self, request):
        context = super().each_context(request)
        context['site_header'] = "🏨 Diamond Hill Resort Admin"
        # Safely obtain a display name for the current user. AnonymousUser does not
        # implement get_full_name(), so check authentication first.
        if getattr(request, 'user', None) and getattr(request.user, 'is_authenticated', False):
            # Use full name when available, otherwise fall back to username
            try:
                context['user_name'] = request.user.get_full_name() or request.user.username
            except Exception:
                context['user_name'] = getattr(request.user, 'username', '')
        else:
            context['user_name'] = ''
        
        # Calculate statistics for dashboard
        stats = {
            'total_rooms': Room.objects.count(),
            'total_bookings': Booking.objects.count(),
            'active_bookings': Booking.objects.filter(payment_status='paid').count(),
            'total_images': GalleryImage.objects.count(),
            'total_posts': BlogPost.objects.filter(is_published=True).count(),
            'total_hero': HeroSection.objects.filter(is_active=True).count(),
        }
        context['stats'] = stats
        return context

admin_site = DiamondHillAdminSite()

class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('hero_icon', 'title', 'image_thumbnail', 'is_active_badge', 'order_display')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    fieldsets = (
        ('🎬 Hero Slide', {
            'fields': ('title', 'subtitle', 'description')
        }), 
        ('📸 Image', {
            'fields': ('image', 'image_preview')
        }), 
        ('⚙️ Settings', {
            'fields': ('order', 'is_active', 'created_at', 'updated_at')
        }),
    )
    
    def hero_icon(self, obj):
        return mark_safe('🎬')
    hero_icon.short_description = 'Type'
    
    def order_display(self, obj):
        return format_html('<strong>#{}</strong>', obj.order)
    order_display.short_description = 'Order'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return mark_safe(
                '<span style="background: #4caf50; color: white; padding: 6px 12px; border-radius: 20px; font-weight: bold;">✅ Active</span>'
            )
        else:
            return mark_safe(
                '<span style="background: #bdbdbd; color: white; padding: 6px 12px; border-radius: 20px; font-weight: bold;">⊘ Inactive</span>'
            )
    is_active_badge.short_description = 'Status'
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="70" height="45" style="border-radius: 5px; object-fit: cover; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"/>',
                obj.image.url
            )
        return '❌'
    image_thumbnail.short_description = 'Preview'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="400" style="border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);"/>',
                obj.image.url
            )
        return 'No Image'
    image_preview.short_description = 'Image Preview'

class RoomImageInline(admin.StackedInline):
    """Inline admin for managing room gallery images."""
    model = RoomImage
    extra = 1
    fields = ('image', 'caption', 'is_primary', 'order', 'image_thumbnail', 'uploaded_at')
    readonly_fields = ('image_thumbnail', 'uploaded_at')
    ordering = ('order', '-uploaded_at')
    
    def image_thumbnail(self, obj):
        """Display image thumbnail in admin."""
        if obj and obj.pk and obj.image:
            html = (
                f'<img src="{obj.image.url}?t={obj.uploaded_at.timestamp()}" width="300" height="250" '
                f'style="border-radius: 8px; object-fit: cover; border: 2px solid #2d8a63; display: block; margin: 10px 0;"/>'
            )
            return mark_safe(html)
        return mark_safe('<span style="color: #999; font-size: 0.9em;">👇 Upload an image above to see preview here</span>')
    image_thumbnail.short_description = '📸 Image Preview'

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_icon', 'title', 'price_display', 'capacity_display', 'image_thumbnail')
    list_display_links = ('title',)  # Make title clickable to edit
    list_filter = ('price', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('slug', 'created_at', 'updated_at', 'image_preview')
    actions = ['mark_featured', 'clear_featured']
    inlines = [RoomImageInline]
    fieldsets = (
        ('🏠 Room Information', {
            'fields': ('title', 'slug', 'description')
        }), 
        ('💰 Pricing & Amenities', {
            'fields': ('price', 'price_usd', 'price_eur', 'amenities', 'max_capacity', 'size_sqft'),
            'description': 'Set prices in different currencies. USD and EUR prices are optional - leave as 0 for auto-conversion from NPR.'
        }), 
        ('📸 Media', {
            'fields': ('image', 'image_preview')
        }), 
        ('📝 Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def room_icon(self, obj):
        return mark_safe('🛏️')
    room_icon.short_description = 'Type'
    
    def price_display(self, obj):
        price_npr = float(obj.price) if obj.price else 0
        price_usd = float(obj.price_usd) if obj.price_usd and obj.price_usd > 0 else float(price_npr) / 130
        price_eur = float(obj.price_eur) if obj.price_eur and obj.price_eur > 0 else float(price_npr) / 140
        
        # Build HTML without format_html to avoid SafeString issues
        html = (
            f'<span style="color: #0d9488; font-weight: bold;">NPR {price_npr:,.0f}</span><br/>'
            f'<small style="color: #666;">$ {price_usd:.2f} | € {price_eur:.2f}</small>'
        )
        return mark_safe(html)
    price_display.short_description = 'Prices'
    
    def capacity_display(self, obj):
        return format_html(
            '👥 {} person{}',
            obj.max_capacity,
            's' if obj.max_capacity > 1 else ''
        )
    capacity_display.short_description = 'Capacity'
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: cover;"/>',
                obj.image.url
            )
        return '❌ No Image'
    image_thumbnail.short_description = 'Preview'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="300" style="border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);"/>',
                obj.image.url
            )
        return 'No Image'
    image_preview.short_description = 'Image Preview'
    
    def mark_featured(self, request, queryset):
        """Bulk action to mark rooms as featured (example)."""
        updated = queryset.update(amenities='Featured')
        self.message_user(request, f'{updated} room(s) marked as featured.')
    mark_featured.short_description = "✨ Mark selected rooms as featured"
    
    def clear_featured(self, request, queryset):
        """Bulk action to clear featured status."""
        updated = queryset.update(amenities='')
        self.message_user(request, f'{updated} room(s) cleared from featured.')
    clear_featured.short_description = "⊘ Clear featured status"

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostForm
    list_display = ('blog_icon', 'title_link', 'author_display', 'status_badge', 'image_thumbnail', 'created_at_display')
    list_filter = ('is_published', 'created_at', 'author')
    search_fields = ('title', 'content', 'excerpt', 'meta_title', 'meta_keywords')
    readonly_fields = ('slug', 'created_at', 'updated_at', 'image_preview')
    date_hierarchy = 'created_at'
    fieldsets = (
        ('📝 Post Information', {
            'fields': ('title', 'slug', 'author')
        }), 
        ('✍️ Content', {
            'fields': ('excerpt', 'content'),
            'classes': ('wide',),
            'description': 'Use the rich text editor below to format your content with bold, italic, headings, lists, and more.'
        }), 
        ('📸 Media', {
            'fields': ('image', 'image_preview')
        }), 
        ('🔍 SEO & Metadata', {
            'description': 'Optimize your blog post for search engines. Leave fields empty to use defaults.',
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }), 
        ('📅 Publication', {
            'fields': ('is_published', 'created_at', 'updated_at')
        }),
    )
    
    def blog_icon(self, obj):
        return mark_safe('📖')
    blog_icon.short_description = 'Type'
    
    def title_link(self, obj):
        """Make title clickable to edit the post."""
        url = reverse('admin:main_blogpost_change', args=[obj.id])
        return format_html(
            '<a href="{}" style="color: #2d8a63; font-weight: 600; text-decoration: none;">{}</a>',
            url,
            obj.title
        )
    title_link.short_description = 'Title'
    
    def author_display(self, obj):
        return format_html('{}', obj.author)
    author_display.short_description = 'Author'
    
    def created_at_display(self, obj):
        return obj.created_at.strftime('%b %d, %Y')
    created_at_display.short_description = 'Published'
    
    def status_badge(self, obj):
        if obj.is_published:
            return mark_safe(
                '<span style="background: #4caf50; color: white; padding: 6px 12px; border-radius: 20px; font-weight: bold;">Published</span>'
            )
        else:
            return mark_safe(
                '<span style="background: #ff9800; color: white; padding: 6px 12px; border-radius: 20px; font-weight: bold;">Draft</span>'
            )
    status_badge.short_description = 'Status'
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: cover;"/>',
                obj.image.url
            )
        return '❌'
    image_thumbnail.short_description = 'Preview'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="400" style="border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);"/>',
                obj.image.url
            )
        return 'No Image'
    image_preview.short_description = 'Image Preview'

class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('gallery_icon', 'caption', 'image_thumbnail', 'upload_date_display', 'image_size')
    list_filter = ('upload_date',)
    search_fields = ('caption',)
    readonly_fields = ('upload_date', 'image_preview')
    fieldsets = (
        ('🖼️ Gallery Item', {
            'fields': ('caption',)
        }), 
        ('📸 Image', {
            'fields': ('image', 'image_preview')
        }), 
        ('📅 Details', {
            'fields': ('upload_date',)
        }),
    )
    date_hierarchy = 'upload_date'
    
    def gallery_icon(self, obj):
        return mark_safe('🖼️')
    gallery_icon.short_description = 'Type'
    
    def upload_date_display(self, obj):
        return obj.upload_date.strftime('%b %d, %Y')
    upload_date_display.short_description = 'Uploaded'
    
    def image_size(self, obj):
        if obj.image:
            try:
                size_kb = obj.image.size / 1024
                if size_kb > 1024:
                    return format_html('<span style="color: #666; font-size: 0.9em;">{}</span>', f'{size_kb / 1024:.1f} MB')
                return format_html('<span style="color: #666; font-size: 0.9em;">{}</span>', f'{size_kb:.0f} KB')
            except:
                return '—'
        return '—'
    image_size.short_description = 'File Size'
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius: 6px; object-fit: cover; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"/>',
                obj.image.url
            )
        return '❌'
    image_thumbnail.short_description = 'Preview'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="400" style="border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);"/>',
                obj.image.url
            )
        return 'No Image'
    image_preview.short_description = 'Image Preview'

class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_badge', 'guest_name', 'room_display', 'date_range', 'payment_status_badge', 'total_amount_display')
    list_filter = ('payment_status', 'room', 'check_in', 'created_at')
    search_fields = ('guest_name', 'guest_email', 'guest_phone')
    readonly_fields = ('created_at', 'updated_at', 'get_nights', 'total_amount_display')
    date_hierarchy = 'check_in'
    fieldsets = (
        ('👤 Guest Information', {
            'fields': ('guest_name', 'guest_email', 'guest_phone')
        }), 
        ('🛏️ Booking Details', {
            'fields': ('room', 'check_in', 'check_out', 'guests', 'get_nights')
        }), 
        ('💳 Pricing & Payment', {
            'fields': ('total_amount', 'total_amount_display', 'currency', 'payment_status')
        }), 
        ('📝 Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def booking_badge(self, obj):
        return format_html(
            '<span style="background: #0d9488; color: white; padding: 5px 10px; border-radius: 20px; font-size: 0.85em;">#{}</span>',
            obj.id
        )
    booking_badge.short_description = '📅 Booking ID'
    
    def room_display(self, obj):
        return format_html('🛏️ {}', obj.room.title)
    room_display.short_description = 'Room'
    
    def date_range(self, obj):
        if obj.check_in and obj.check_out:
            return format_html(
                '{} → {}',
                obj.check_in.strftime('%b %d'),
                obj.check_out.strftime('%b %d, %Y')
            )
        return '—'
    date_range.short_description = 'Dates'
    
    def get_nights(self, obj):
        nights = obj.get_number_of_nights()
        if nights > 0:
            return format_html('🌙 {} night{}', nights, 's' if nights > 1 else '')
        return '—'
    get_nights.short_description = 'Duration'
    
    def total_amount_display(self, obj):
        if obj.total_amount:
            amount = f"{float(obj.total_amount):,.0f}"
            return format_html(
                '<span style="color: #0d9488; font-weight: bold; font-size: 1.1em;">NPR {}</span>',
                amount
            )
        return '—'
    total_amount_display.short_description = 'Total Amount'
    
    def payment_status_badge(self, obj):
        colors = {
            'pending': '#ff9800',
            'paid': '#4caf50',
            'confirmed': '#2196f3',
            'cancelled': '#f44336'
        }
        status_icons = {
            'pending': '⏳',
            'paid': '✅',
            'confirmed': '✔️',
            'cancelled': '❌'
        }
        color = colors.get(obj.payment_status, '#9e9e9e')
        icon = status_icons.get(obj.payment_status, '•')
        return format_html(
            '<span style="background: {}; color: white; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9em;">{} {}</span>',
            color,
            icon,
            obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Payment Status'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_icon', 'guest_name', 'location_display', 'rating_stars', 'publish_badge', 'created_at_display')
    list_display_links = ('guest_name',)  # Make guest_name clickable to edit
    list_filter = ('is_published', 'rating', 'created_at')
    search_fields = ('guest_name', 'location', 'review_text')
    readonly_fields = ('created_at', 'updated_at', 'review_preview')
    actions = ['publish_reviews', 'unpublish_reviews']
    date_hierarchy = 'created_at'
    fieldsets = (
        ('⭐ Review Information', {
            'fields': ('guest_name', 'location', 'rating', 'visited_date')
        }), 
        ('💬 Review Content', {
            'fields': ('review_text',),
            'classes': ('wide',)
        }), 
        ('📋 Publication', {
            'fields': ('is_published', 'created_at', 'updated_at')
        }),
        ('👁️ Preview', {
            'fields': ('review_preview',),
            'classes': ('collapse',)
        }),
    )
    
    def review_icon(self, obj):
        return mark_safe('⭐')
    review_icon.short_description = 'Type'
    
    def location_display(self, obj):
        if obj.location:
            return format_html('📍 {}', obj.location)
        return '—'
    location_display.short_description = 'Location'
    
    def created_at_display(self, obj):
        return obj.created_at.strftime('%b %d, %Y')
    created_at_display.short_description = 'Date'
    
    def rating_stars(self, obj):
        stars = '⭐' * obj.rating
        return format_html('<span style="color: #ffc107; font-size: 1.1em;">{}</span>', stars)
    rating_stars.short_description = 'Rating'
    
    def publish_badge(self, obj):
        if obj.is_published:
            return mark_safe(
                '<span style="background: #4caf50; color: white; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 0.85em;">✅ Published</span>'
            )
        else:
            return mark_safe(
                '<span style="background: #bdbdbd; color: white; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 0.85em;">⏳ Draft</span>'
            )
    publish_badge.short_description = 'Status'
    
    def review_preview(self, obj):
        if obj.guest_name and obj.review_text:
            return format_html(
                '<div style="background: #f5f5f5; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;"><strong>{}</strong><br><em>"{}"</em><br><small style="color: #666;">⭐ {} stars • {} ({})</small></div>',
                obj.guest_name,
                obj.review_text,
                obj.rating,
                obj.location if obj.location else 'Unknown',
                obj.created_at.strftime('%b %d, %Y')
            )
        return '<p style="color: #999;">Review data incomplete</p>'
    review_preview.short_description = 'Preview'
    
    def publish_reviews(self, request, queryset):
        """Bulk action to publish reviews."""
        updated = queryset.update(is_published=True)
        self.message_user(request, f'✅ {updated} review(s) published.')
    publish_reviews.short_description = "✅ Publish selected reviews"
    
    def unpublish_reviews(self, request, queryset):
        """Bulk action to unpublish reviews."""
        updated = queryset.update(is_published=False)
        self.message_user(request, f'⏳ {updated} review(s) unpublished.')
    unpublish_reviews.short_description = "⏳ Unpublish selected reviews"

class AboutAdmin(admin.ModelAdmin):
    """Admin interface for managing About page content."""
    list_display = ('about_icon', 'title', 'image_thumbnail', 'last_updated')
    readonly_fields = ('updated_at', 'image_preview')
    fieldsets = (
        ('📝 About Page Content', {
            'fields': ('title',),
            'description': 'Main page title'
        }),
        ('🖼️ Featured Image', {
            'fields': ('image', 'image_preview'),
            'description': 'Image displayed on homepage About section'
        }),
        ('📖 Our Story Section', {
            'fields': ('story',),
            'classes': ('wide',),
            'description': 'Main "Our Story" content that appears on the About page'
        }),
        ('💡 Values Section', {
            'fields': ('values_intro',),
            'classes': ('wide',),
            'description': 'Optional introduction before the values section'
        }),
        ('📅 Last Updated', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    def about_icon(self, obj):
        return mark_safe('📄')
    about_icon.short_description = 'Type'
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: cover;"/>',
                obj.image.url
            )
        return '❌ No Image'
    image_thumbnail.short_description = 'Preview'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="400" style="border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);"/>',
                obj.image.url
            )
        return 'No Image - Upload one to display on homepage'
    image_preview.short_description = 'Image Preview'
    
    def last_updated(self, obj):
        return obj.updated_at.strftime('%b %d, %Y at %I:%M %p')
    last_updated.short_description = 'Last Modified'
    
    def has_add_permission(self, request):
        """Allow adding only if there's no existing About page."""
        return not About.objects.exists()

admin_site.register(HeroSection, HeroSectionAdmin)
admin_site.register(Room, RoomAdmin)
admin_site.register(BlogPost, BlogPostAdmin)
admin_site.register(GalleryImage, GalleryImageAdmin)
admin_site.register(Booking, BookingAdmin)
admin_site.register(Review, ReviewAdmin)
admin_site.register(About, AboutAdmin)


class RoomInventoryAdmin(admin.ModelAdmin):
    """Admin interface for managing room inventory."""
    list_display = ('inventory_icon', 'room_display', 'inventory_status', 'total_rooms_display', 'available_display')
    list_display_links = ('room_display',)
    list_filter = ('room__title',)
    search_fields = ('room__title',)
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('🛏️ Room Inventory Management', {
            'fields': ('room', 'total_rooms', 'available_rooms', 'updated_at'),
            'description': 'Manage room count and availability. Available rooms are calculated automatically based on bookings.'
        }),
    )
    
    def inventory_icon(self, obj):
        return mark_safe('📦')
    inventory_icon.short_description = 'Type'
    
    def room_display(self, obj):
        return format_html('🛏️ {}', obj.room.title)
    room_display.short_description = 'Room Type'
    
    def total_rooms_display(self, obj):
        return format_html(
            '<span style="background: #2196f3; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">{}</span>',
            obj.total_rooms
        )
    total_rooms_display.short_description = 'Total Rooms'
    
    def available_display(self, obj):
        if obj.available_rooms > 0:
            color = '#4caf50'
            icon = '✅'
        else:
            color = '#f44336'
            icon = '❌'
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 4px; font-weight: bold;">{} {}</span>',
            color,
            icon,
            obj.available_rooms
        )
    available_display.short_description = 'Available'
    
    def inventory_status(self, obj):
        percentage = (obj.available_rooms / obj.total_rooms) * 100 if obj.total_rooms > 0 else 0
        
        if percentage > 50:
            status_color = '#4caf50'
            status = 'Plenty'
        elif percentage > 20:
            status_color = '#ff9800'
            status = 'Limited'
        else:
            status_color = '#f44336'
            status = 'Critical'
        
        return format_html(
            '<span style="background: {}; color: white; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 0.9em;">⚠️ {}</span>',
            status_color,
            status
        )
    inventory_status.short_description = 'Status'


admin_site.register(RoomInventory, RoomInventoryAdmin)
