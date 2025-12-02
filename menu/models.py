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
    
    def check_and_update_status(self):
        """Auto-update status if estimated time has passed"""
        if self.status in ['completed', 'cancelled']:
            return
        
        if self.estimated_ready_time:
            now = timezone.now()
            # If time has passed and still pending/confirmed, update to ready
            if now >= self.estimated_ready_time:
                if self.status in ['pending', 'confirmed']:
                    self.status = 'ready'
                    self.save()
                elif self.status == 'preparing':
                    # If preparing and time passed, mark as ready
                    self.status = 'ready'
                    self.save()


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


class Feedback(models.Model):
    """Customer feedback/review model"""
    RATING_CHOICES = [
        (5, '⭐⭐⭐⭐⭐ Excellent'),
        (4, '⭐⭐⭐⭐ Very Good'),
        (3, '⭐⭐⭐ Good'),
        (2, '⭐⭐ Fair'),
        (1, '⭐ Poor'),
    ]
    
    order = models.ForeignKey(Order, related_name='feedbacks', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # For moderation
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Feedbacks'
    
    def __str__(self):
        return f"Feedback for Order #{self.order.id} - {self.rating} stars"
    
    def get_rating_stars(self):
        """Get star display for rating"""
        return '⭐' * self.rating


class NewsletterSubscriber(models.Model):
    """Newsletter subscription model"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    """Contact form submission model"""
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('feedback', 'Feedback'),
        ('complaint', 'Complaint'),
        ('partnership', 'Partnership'),
        ('event', 'Event Booking'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='general')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class SpecialOffer(models.Model):
    """Special offers and promotions"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    discount_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    code = models.CharField(max_length=50, unique=True, blank=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    image = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def is_valid(self):
        """Check if offer is currently valid"""
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_until


class Reservation(models.Model):
    """Table/Event reservation model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    EVENT_TYPE_CHOICES = [
        ('table', 'Table Reservation'),
        ('event', 'Private Event'),
        ('meeting', 'Meeting Room'),
        ('party', 'Birthday Party'),
        ('other', 'Other'),
    ]
    
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, default='table')
    reservation_date = models.DateTimeField()
    number_of_guests = models.PositiveIntegerField(default=2)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['reservation_date']
    
    def __str__(self):
        return f"Reservation for {self.customer_name} on {self.reservation_date.date()}"


class FAQ(models.Model):
    """Frequently Asked Questions"""
    question = models.CharField(max_length=500)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'question']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
    
    def __str__(self):
        return self.question


class GalleryImage(models.Model):
    """Gallery images for the coffee shop"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500)
    category = models.CharField(max_length=100, blank=True, default='general')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name_plural = 'Gallery Images'
    
    def __str__(self):
        return self.title
