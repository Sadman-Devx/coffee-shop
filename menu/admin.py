from datetime import datetime

from django.contrib import admin
from django.db.models import DecimalField, ExpressionWrapper, F, Sum, Value
from django.db.models.functions import Coalesce
from django.template.response import TemplateResponse
from django.urls import path
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
    list_display = [
        'id',
        'customer_name',
        'customer_email',
        'status',
        'delivery_option',
        'payment_method',
        'final_amount',
        'created_at'
    ]
    list_filter = ['status', 'delivery_option', 'payment_method', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone', 'discount_code']
    readonly_fields = ['created_at', 'updated_at', 'total_amount', 'final_amount', 'discount_amount', 'delivery_fee']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Fulfillment & Payment', {
            'fields': ('delivery_option', 'payment_method', 'payment_status', 'status')
        }),
        ('Financials', {
            'fields': ('total_amount', 'discount_code', 'discount_amount', 'delivery_fee', 'final_amount')
        }),
        ('Order Details', {
            'fields': ('estimated_ready_time', 'notes', 'completion_message', 'created_at', 'updated_at')
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "monthly-sales/",
                self.admin_site.admin_view(self.monthly_sales_view),
                name="menu_order_monthly_sales",
            ),
        ]
        return custom_urls + urls

    def monthly_sales_view(self, request):
        today = timezone.localdate()
        year = int(request.GET.get("year", today.year))
        month = int(request.GET.get("month", today.month))

        start = timezone.make_aware(datetime(year, month, 1))
        if month == 12:
            end = timezone.make_aware(datetime(year + 1, 1, 1))
        else:
            end = timezone.make_aware(datetime(year, month + 1, 1))

        orders_qs = (
            Order.objects.filter(created_at__gte=start, created_at__lt=end)
            .exclude(status="cancelled")
            .prefetch_related("items__coffee")
            .order_by("-created_at")
        )

        items_qs = OrderItem.objects.filter(order__in=orders_qs).select_related("coffee")

        line_total = ExpressionWrapper(
            F("quantity") * F("price"),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )
        zero_money = Value(0, output_field=DecimalField(max_digits=12, decimal_places=2))

        totals = items_qs.aggregate(
            items_sold=Coalesce(Sum("quantity"), 0),
            revenue=Coalesce(
                Sum(line_total),
                zero_money,
            ),
        )

        per_coffee = (
            items_qs.values("coffee__id", "coffee__name")
            .annotate(
                qty=Coalesce(Sum("quantity"), 0),
                revenue=Coalesce(
                    Sum(line_total),
                    zero_money,
                ),
            )
            .order_by("-qty", "coffee__name")
        )

        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "title": "Monthly sales report",
            "year": year,
            "month": month,
            "start": start,
            "end": end,
            "orders": orders_qs,
            "per_coffee": per_coffee,
            "totals": totals,
        }
        return TemplateResponse(request, "admin/menu/monthly_sales_report.html", context)
    
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
