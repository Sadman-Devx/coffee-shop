from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from .models import Coffee, Order, OrderItem, Feedback
import json


def get_cart(request):
    """Get cart from session"""
    cart = request.session.get('cart', {})
    return cart


def get_cart_count(request):
    """Get total number of items in cart"""
    cart = get_cart(request)
    return sum(item.get('quantity', 0) for item in cart.values())


def get_cart_total(request):
    """Calculate total price of items in cart"""
    cart = get_cart(request)
    total = 0
    for coffee_id, item in cart.items():
        try:
            coffee = Coffee.objects.get(id=int(coffee_id), available=True)
            total += float(coffee.price) * item.get('quantity', 0)
        except Coffee.DoesNotExist:
            continue
    return total


def home(request):
    """Render the main landing page with featured menu items."""
    # Get search and filter parameters
    search_query = request.GET.get('search', '').strip()
    filter_origin = request.GET.get('origin', '').strip()
    filter_strength = request.GET.get('strength', '').strip()
    sort_by = request.GET.get('sort', 'name')
    
    # Optimize query - only fetch available coffees
    coffees = Coffee.objects.filter(available=True)
    
    # Apply search filter
    if search_query:
        coffees = coffees.filter(
            models.Q(name__icontains=search_query) |
            models.Q(notes__icontains=search_query) |
            models.Q(origin__icontains=search_query)
        )
    
    # Apply origin filter
    if filter_origin:
        coffees = coffees.filter(origin__icontains=filter_origin)
    
    # Apply strength filter
    if filter_strength:
        coffees = coffees.filter(strength__icontains=filter_strength)
    
    # Apply sorting
    if sort_by == 'price_low':
        coffees = coffees.order_by('price')
    elif sort_by == 'price_high':
        coffees = coffees.order_by('-price')
    else:
        coffees = coffees.order_by('name')
    
    # Get unique origins and strengths for filter dropdowns
    all_origins = Coffee.objects.filter(available=True).values_list('origin', flat=True).distinct()
    all_strengths = Coffee.objects.filter(available=True).values_list('strength', flat=True).distinct()
    
    highlights = {
        "tagline": "Small-batch roasting, all-day hospitality.",
        "hours": "Mon–Fri 7a–7p · Sat–Sun 8a–6p",
        "address": "214 Brewed Awakening Lane · River City",
        "phone": "(555) 322-8890",
    }

    experiences = [
        "Reserve tastings every Friday night",
        "Latte art classes twice a month",
        "Seasonal beans roasted in-house",
    ]

    testimonials = [
        {
            "name": "Camila R.",
            "quote": "Richest espresso in town and the warmest baristas.",
        },
        {
            "name": "Evan L.",
            "quote": "The Cascara Tonic is my go-to afternoon reset.",
        },
    ]

    context = {
        "coffees": coffees,
        "highlights": highlights,
        "experiences": experiences,
        "testimonials": testimonials,
        "cart_count": get_cart_count(request),
        "search_query": search_query,
        "filter_origin": filter_origin,
        "filter_strength": filter_strength,
        "sort_by": sort_by,
        "all_origins": all_origins,
        "all_strengths": all_strengths,
    }
    return render(request, "menu/home.html", context)


@require_POST
def add_to_cart(request, coffee_id):
    """Add coffee item to cart"""
    coffee = get_object_or_404(Coffee, id=coffee_id, available=True)
    cart = get_cart(request)
    
    coffee_id_str = str(coffee_id)
    if coffee_id_str in cart:
        cart[coffee_id_str]['quantity'] += 1
        action = 'updated'
    else:
        cart[coffee_id_str] = {
            'quantity': 1,
            'name': coffee.name,
            'price': str(coffee.price),
        }
        action = 'added'
    
    request.session['cart'] = cart
    request.session.modified = True  # Ensure session is saved
    
    cart_count = get_cart_count(request)
    cart_total = get_cart_total(request)
    
    # Always return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({
            'success': True,
            'cart_count': cart_count,
            'cart_total': f"{cart_total:.2f}",
            'message': f"{coffee.name} {action} to cart!",
            'action': action
        })
    
    messages.success(request, f"{coffee.name} added to cart!")
    return redirect('home')


def view_cart(request):
    """Display shopping cart"""
    cart = get_cart(request)
    cart_items = []
    total = 0
    
    for coffee_id, item in cart.items():
        try:
            coffee = Coffee.objects.get(id=int(coffee_id), available=True)
            quantity = item.get('quantity', 1)
            subtotal = float(coffee.price) * quantity
            total += subtotal
            
            cart_items.append({
                'coffee': coffee,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Coffee.DoesNotExist:
            continue
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/cart.html", context)


@require_POST
def update_cart(request, coffee_id):
    """Update quantity of item in cart"""
    coffee = get_object_or_404(Coffee, id=coffee_id, available=True)
    cart = get_cart(request)
    coffee_id_str = str(coffee_id)
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity <= 0:
        if coffee_id_str in cart:
            del cart[coffee_id_str]
            message = f"{coffee.name} removed from cart"
            messages.success(request, message)
    else:
        if coffee_id_str in cart:
            cart[coffee_id_str]['quantity'] = quantity
            message = f"{coffee.name} quantity updated"
            messages.success(request, message)
    
    request.session['cart'] = cart
    request.session.modified = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': get_cart_count(request),
            'cart_total': f"{get_cart_total(request):.2f}",
            'message': message if 'message' in locals() else 'Cart updated'
        })
    
    return redirect('view_cart')


@require_POST
def remove_from_cart(request, coffee_id):
    """Remove item from cart"""
    coffee = get_object_or_404(Coffee, id=coffee_id)
    cart = get_cart(request)
    coffee_id_str = str(coffee_id)
    
    if coffee_id_str in cart:
        del cart[coffee_id_str]
        message = f"{coffee.name} removed from cart"
        messages.success(request, message)
    
    request.session['cart'] = cart
    request.session.modified = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': get_cart_count(request),
            'cart_total': f"{get_cart_total(request):.2f}",
            'message': message
        })
    
    return redirect('view_cart')


def checkout(request):
    """Display checkout page"""
    cart = get_cart(request)
    if not cart:
        messages.warning(request, "Your cart is empty!")
        return redirect('view_cart')
    
    cart_items = []
    total = 0
    
    for coffee_id, item in cart.items():
        try:
            coffee = Coffee.objects.get(id=int(coffee_id), available=True)
            quantity = item.get('quantity', 1)
            subtotal = float(coffee.price) * quantity
            total += subtotal
            
            cart_items.append({
                'coffee': coffee,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Coffee.DoesNotExist:
            continue
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/checkout.html", context)


@require_POST
def place_order(request):
    """Process order placement"""
    cart = get_cart(request)
    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('view_cart')
    
    # Get customer information
    customer_name = request.POST.get('customer_name', '').strip()
    customer_email = request.POST.get('customer_email', '').strip()
    customer_phone = request.POST.get('customer_phone', '').strip()
    notes = request.POST.get('notes', '').strip()
    
    # Validate required fields
    if not all([customer_name, customer_email, customer_phone]):
        messages.error(request, "Please fill in all required fields!")
        return redirect('checkout')
    
    # Create order
    order = Order.objects.create(
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone=customer_phone,
        notes=notes,
        status='pending'
    )
    
    # Create order items
    total = 0
    for coffee_id, item in cart.items():
        try:
            coffee = Coffee.objects.get(id=int(coffee_id), available=True)
            quantity = item.get('quantity', 1)
            subtotal = float(coffee.price) * quantity
            total += subtotal
            
            OrderItem.objects.create(
                order=order,
                coffee=coffee,
                quantity=quantity,
                price=coffee.price
            )
        except Coffee.DoesNotExist:
            continue
    
    # Update order total and calculate estimated time
    order.total_amount = total
    order.calculate_estimated_time()
    order.save()
    
    # Store order ID in session for tracking
    request.session['last_order_id'] = order.id
    
    # Clear cart
    request.session['cart'] = {}
    
    messages.success(request, f"Order #{order.id} placed successfully! We'll contact you soon.")
    return redirect('order_confirmation', order_id=order.id)


def order_confirmation(request, order_id):
    """Display order confirmation page"""
    # Optimize query
    order = get_object_or_404(
        Order.objects.prefetch_related('items__coffee'),
        id=order_id
    )
    # Auto-update status if time has passed
    order.check_and_update_status()
    time_remaining = order.get_time_remaining()
    
    # Check if feedback already submitted
    has_feedback = order.feedbacks.exists()
    
    context = {
        'order': order,
        'time_remaining': time_remaining,
        'has_feedback': has_feedback,
        'cart_count': 0,
    }
    return render(request, "menu/order_confirmation.html", context)


def track_order(request, order_id):
    """Display order tracking page"""
    # Optimize query - prefetch related items to avoid N+1 queries
    order = get_object_or_404(
        Order.objects.prefetch_related('items__coffee'),
        id=order_id
    )
    # Auto-update status if time has passed
    order.check_and_update_status()
    time_remaining = order.get_time_remaining()
    
    # Check if feedback already submitted
    has_feedback = order.feedbacks.exists()
    
    context = {
        'order': order,
        'time_remaining': time_remaining,
        'has_feedback': has_feedback,
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/track_order.html", context)


def my_orders(request):
    """Display user's orders by email or phone"""
    email = request.GET.get('email', '').strip()
    phone = request.GET.get('phone', '').strip()
    orders = None
    
    # Optimize queries with prefetch_related
    if email:
        orders = Order.objects.filter(
            customer_email=email
        ).prefetch_related('items__coffee').order_by('-created_at')
    elif phone:
        orders = Order.objects.filter(
            customer_phone=phone
        ).prefetch_related('items__coffee').order_by('-created_at')
    
    # Auto-update status for all orders if time has passed
    if orders:
        for order in orders:
            order.check_and_update_status()
    
    context = {
        'orders': orders,
        'email': email,
        'phone': phone,
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/my_orders.html", context)


def send_order_completion_notification(order):
    """Send notification when order is completed"""
    if order.status == 'completed' and order.completion_message:
        subject = f"Your Order #{order.id} is Ready! ☕"
        message = f"""
Hello {order.customer_name},

Great news! Your order is ready for pickup!

{order.completion_message}

Order Details:
- Order #: {order.id}
- Total: ${order.total_amount}
- Status: {order.get_status_display()}

Thank you for choosing Brew Bloom Coffee!

Best regards,
Brew Bloom Coffee Team
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [order.customer_email],
                fail_silently=True,
            )
        except Exception as e:
            # Email sending failed, but we'll still show the message on the site
            pass


@require_POST
def submit_feedback(request, order_id):
    """Submit customer feedback for an order"""
    order = get_object_or_404(Order, id=order_id)
    
    # Check if feedback already exists
    if order.feedbacks.exists():
        messages.warning(request, "You have already submitted feedback for this order.")
        return redirect('track_order', order_id=order_id)
    
    # Get feedback data
    customer_name = request.POST.get('customer_name', '').strip()
    customer_email = request.POST.get('customer_email', '').strip()
    rating = int(request.POST.get('rating', 0))
    comment = request.POST.get('comment', '').strip()
    
    # Validate
    if not all([customer_name, customer_email, rating]):
        messages.error(request, "Please fill in all required fields!")
        return redirect('track_order', order_id=order_id)
    
    if rating < 1 or rating > 5:
        messages.error(request, "Please select a valid rating!")
        return redirect('track_order', order_id=order_id)
    
    # Verify email matches order
    if customer_email.lower() != order.customer_email.lower():
        messages.error(request, "Email does not match the order. Please use the email used for this order.")
        return redirect('track_order', order_id=order_id)
    
    # Create feedback
    feedback = Feedback.objects.create(
        order=order,
        customer_name=customer_name,
        customer_email=customer_email,
        rating=rating,
        comment=comment,
        approved=True  # Auto-approve for now
    )
    
    messages.success(request, "Thank you for your feedback! We appreciate your input.")
    return redirect('track_order', order_id=order_id)


def view_feedbacks(request):
    """Display all approved feedbacks"""
    feedbacks = Feedback.objects.filter(approved=True).select_related('order').order_by('-created_at')[:10]
    
    context = {
        'feedbacks': feedbacks,
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/feedbacks.html", context)
