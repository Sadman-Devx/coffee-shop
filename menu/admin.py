from django.contrib import admin
from .models import Coffee, Order, OrderItem


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
    list_display = ['id', 'customer_name', 'customer_email', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Order Details', {
            'fields': ('status', 'total_amount', 'notes', 'created_at', 'updated_at')
        }),
    )
