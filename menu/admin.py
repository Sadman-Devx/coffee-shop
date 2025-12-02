from django.contrib import admin
from django.utils import timezone
from .models import (Coffee, Order, OrderItem, Feedback, NewsletterSubscriber, 
                     ContactMessage, SpecialOffer, Reservation, FAQ, GalleryImage)
from .views import send_order_completion_notification


@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'origin', 'strength', 'available']
    list_filter = ['available', 'origin', 'strength']
    search_fields = ['name', 'origin', 'notes']
    list_editable = ['available']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'status', 'total_amount', 'estimated_ready_time', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Order Details', {
            'fields': ('status', 'total_amount', 'estimated_ready_time', 'notes', 'completion_message', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Override save to send notification when order is completed"""
        if change:
            # Get the old status
            old_order = Order.objects.get(pk=obj.pk)
            old_status = old_order.status
            
            # If status changed to completed, send notification
            if old_status != 'completed' and obj.status == 'completed':
                if not obj.completion_message:
                    obj.completion_message = f"Your order #{obj.id} is ready for pickup! Please come to our store to collect your order. Thank you for your patience!"
                send_order_completion_notification(obj)
        
        super().save_model(request, obj, form, change)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['order', 'customer_name', 'rating', 'approved', 'created_at']
    list_filter = ['approved', 'rating', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'comment', 'order__id']
    list_editable = ['approved']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Order Information', {
            'fields': ('order',)
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email')
        }),
        ('Feedback', {
            'fields': ('rating', 'comment', 'approved', 'created_at')
        }),
    )


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name']
    list_editable = ['is_active']
    readonly_fields = ['subscribed_at']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'subject', 'created_at']
    search_fields = ['name', 'email', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message', 'is_read', 'created_at')
        }),
    )


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount_percentage', 'code', 'is_active', 'valid_from', 'valid_until']
    list_filter = ['is_active', 'valid_from', 'valid_until']
    search_fields = ['title', 'description', 'code']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Offer Details', {
            'fields': ('title', 'description', 'image')
        }),
        ('Discount', {
            'fields': ('discount_percentage', 'code')
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_until', 'is_active', 'created_at')
        }),
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'event_type', 'reservation_date', 'number_of_guests', 'status']
    list_filter = ['status', 'event_type', 'reservation_date']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Reservation Details', {
            'fields': ('event_type', 'reservation_date', 'number_of_guests', 'special_requests')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'category', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured']
    readonly_fields = ['created_at']
