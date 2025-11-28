from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from datetime import timedelta


class Coffee(models.Model):
    """Coffee menu item model"""
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    origin = models.CharField(max_length=200)
    strength = models.CharField(max_length=100)
    notes = models.TextField()
    image = models.URLField(max_length=500, blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Coffees'

    def __str__(self):
        return self.name


class Order(models.Model):
    """Customer order model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

    def calculate_total(self):
        """Calculate total from order items"""
        return sum(item.subtotal() for item in self.items.all())
    
    def get_estimated_time(self):
        """Calculate estimated delivery/preparation time based on status"""
        if self.status == 'completed':
            return "Delivered"
        elif self.status == 'cancelled':
            return "Cancelled"
        
        # Base preparation time: 15 minutes
        base_time = 15
        
        # Add time based on number of items
        item_count = sum(item.quantity for item in self.items.all())
        additional_time = (item_count - 1) * 3  # 3 minutes per additional item
        
        # Status-based adjustments
        status_times = {
            'pending': base_time + additional_time,
            'confirmed': base_time + additional_time - 2,
            'preparing': base_time + additional_time - 5,
            'ready': 0,
        }
        
        estimated_minutes = status_times.get(self.status, base_time + additional_time)
        
        if estimated_minutes <= 0:
            return "Ready for pickup"
        elif estimated_minutes < 60:
            return f"{estimated_minutes} minutes"
        else:
            hours = estimated_minutes // 60
            minutes = estimated_minutes % 60
            if minutes > 0:
                return f"{hours}h {minutes}m"
            return f"{hours} hour{'s' if hours > 1 else ''}"
    
    def get_status_display_class(self):
        """Get CSS class for status badge"""
        status_classes = {
            'pending': 'status-pending',
            'confirmed': 'status-confirmed',
            'preparing': 'status-preparing',
            'ready': 'status-ready',
            'completed': 'status-completed',
            'cancelled': 'status-cancelled',
        }
        return status_classes.get(self.status, 'status-pending')


class OrderItem(models.Model):
    """Individual item in an order"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def subtotal(self):
        """Calculate subtotal for this item"""
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity}x {self.coffee.name}"
