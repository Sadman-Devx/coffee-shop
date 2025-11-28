from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import models
from .models import Coffee, Order, OrderItem
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
    coffees = Coffee.objects.filter(available=True)
    
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
    else:
        cart[coffee_id_str] = {
            'quantity': 1,
            'name': coffee.name,
            'price': str(coffee.price),
        }
    
    request.session['cart'] = cart
    messages.success(request, f"{coffee.name} added to cart!")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': get_cart_count(request),
            'message': f"{coffee.name} added to cart!"
        })
    
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
            messages.success(request, f"{coffee.name} removed from cart")
    else:
        if coffee_id_str in cart:
            cart[coffee_id_str]['quantity'] = quantity
            messages.success(request, f"{coffee.name} quantity updated")
    
    request.session['cart'] = cart
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': get_cart_count(request),
            'cart_total': get_cart_total(request),
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
        messages.success(request, f"{coffee.name} removed from cart")
    
    request.session['cart'] = cart
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
    
    # Update order total
    order.total_amount = total
    order.save()
    
    # Clear cart
    request.session['cart'] = {}
    
    messages.success(request, f"Order #{order.id} placed successfully! We'll contact you soon.")
    return redirect('order_confirmation', order_id=order.id)


def order_confirmation(request, order_id):
    """Display order confirmation page"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'cart_count': 0,
    }
    return render(request, "menu/order_confirmation.html", context)


def track_orders(request):
    """Display order tracking page - search by email or phone"""
    orders = None
    search_query = None
    
    if request.method == 'POST':
        search_query = request.POST.get('search', '').strip()
        if search_query:
            # Search by email or phone
            orders = Order.objects.filter(
                models.Q(customer_email__icontains=search_query) |
                models.Q(customer_phone__icontains=search_query)
            ).order_by('-created_at')[:10]  # Limit to 10 most recent
    
    context = {
        'orders': orders,
        'search_query': search_query,
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/track_orders.html", context)


def view_order(request, order_id):
    """View detailed order information"""
    order = get_object_or_404(Order, id=order_id)
    
    context = {
        'order': order,
        'estimated_time': order.get_estimated_time(),
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/view_order.html", context)
