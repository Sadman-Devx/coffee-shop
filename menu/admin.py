from django.contrib import admin
from django.utils import timezone
from .models import Coffee, Order, OrderItem
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
