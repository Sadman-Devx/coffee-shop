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
    estimated_ready_time = models.DateTimeField(null=True, blank=True)
    completion_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

    def calculate_total(self):
        """Calculate total from order items"""
        return sum(item.subtotal() for item in self.items.all())
    
    def calculate_estimated_time(self):
        """Calculate estimated ready time based on order items"""
        # Base time: 5 minutes
        base_minutes = 5
        # Add 2 minutes per item
        item_count = sum(item.quantity for item in self.items.all())
        total_minutes = base_minutes + (item_count * 2)
        
        if not self.estimated_ready_time:
            self.estimated_ready_time = timezone.now() + timedelta(minutes=total_minutes)
            self.save()
        
        return self.estimated_ready_time
    
    def get_time_remaining(self):
        """Get remaining time until order is ready"""
        if not self.estimated_ready_time:
            self.calculate_estimated_time()
        
        if self.status in ['completed', 'cancelled']:
            return None
        
        now = timezone.now()
        if self.estimated_ready_time > now:
            delta = self.estimated_ready_time - now
            minutes = int(delta.total_seconds() / 60)
            return minutes
        return 0
    
    def get_status_display_class(self):
        """Get CSS class for status display"""
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
