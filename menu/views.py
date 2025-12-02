from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.utils import timezone
from .models import (Coffee, Order, OrderItem, Feedback, NewsletterSubscriber, 
                     ContactMessage, SpecialOffer, Reservation, FAQ, GalleryImage)
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
    """Display all approved feedbacks with improved efficiency"""
    # Get all approved feedbacks with optimized query
    feedbacks = Feedback.objects.filter(approved=True).select_related('order').order_by('-created_at')
    
    # Calculate average rating - fix: use the queryset before slicing
    total_count = feedbacks.count()
    
    if total_count > 0:
        avg_rating = feedbacks.aggregate(models.Avg('rating'))['rating__avg'] or 0
        avg_rating = round(avg_rating, 1)
        
        # Get rating distribution - optimized: use single query with values()
        from django.db.models import Count
        rating_distribution = feedbacks.values('rating').annotate(count=Count('id'))
        rating_counts = {i: 0 for i in range(5, 0, -1)}
        for item in rating_distribution:
            rating_counts[item['rating']] = item['count']
    else:
        avg_rating = 0
        rating_counts = {i: 0 for i in range(5, 0, -1)}
    
    # Get recent feedbacks (last 20)
    recent_feedbacks = list(feedbacks[:20])
    
    context = {
        'feedbacks': recent_feedbacks,
        'avg_rating': avg_rating,
        'total_reviews': total_count,
        'rating_counts': rating_counts,
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/feedbacks.html", context)


def about_us(request):
    """About Us page"""
    context = {
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/about_us.html", context)


@require_http_methods(["GET", "POST"])
def contact_us(request):
    """Contact Us page with form"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', 'general')
        message = request.POST.get('message', '').strip()
        
        if not all([name, email, message]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('contact_us')
    
    context = {
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/contact_us.html", context)


def location_hours(request):
    """Location and Hours page"""
    context = {
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/location_hours.html", context)


@require_http_methods(["POST"])
def newsletter_subscribe(request):
    """Newsletter subscription"""
    email = request.POST.get('email', '').strip()
    name = request.POST.get('name', '').strip()
    
    if not email:
        return JsonResponse({'success': False, 'message': 'Email is required.'})
    
    subscriber, created = NewsletterSubscriber.objects.get_or_create(
        email=email,
        defaults={'name': name, 'is_active': True}
    )
    
    if not created:
        if subscriber.is_active:
            return JsonResponse({'success': False, 'message': 'You are already subscribed!'})
        else:
            subscriber.is_active = True
            subscriber.name = name
            subscriber.save()
    
    return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})


def special_offers(request):
    """Special Offers page"""
    now = timezone.now()
    offers = SpecialOffer.objects.filter(
        is_active=True,
        valid_from__lte=now,
        valid_until__gte=now
    ).order_by('-created_at')
    
    context = {
        'offers': offers,
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/special_offers.html", context)


def gallery(request):
    """Gallery page"""
    images = GalleryImage.objects.all().order_by('-is_featured', '-created_at')
    categories = GalleryImage.objects.values_list('category', flat=True).distinct()
    
    context = {
        'images': images,
        'categories': categories,
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/gallery.html", context)


def faq(request):
    """FAQ page"""
    faqs = FAQ.objects.filter(is_active=True).order_by('order', 'question')
    
    context = {
        'faqs': faqs,
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/faq.html", context)


@require_http_methods(["GET", "POST"])
def make_reservation(request):
    """Reservation booking page"""
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        customer_email = request.POST.get('customer_email', '').strip()
        customer_phone = request.POST.get('customer_phone', '').strip()
        event_type = request.POST.get('event_type', 'table')
        reservation_date = request.POST.get('reservation_date', '').strip()
        reservation_time = request.POST.get('reservation_time', '').strip()
        number_of_guests = request.POST.get('number_of_guests', '2')
        special_requests = request.POST.get('special_requests', '').strip()
        
        if not all([customer_name, customer_email, customer_phone, reservation_date, reservation_time]):
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                from datetime import datetime
                datetime_str = f"{reservation_date} {reservation_time}"
                reservation_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                reservation_datetime = timezone.make_aware(reservation_datetime)
                
                Reservation.objects.create(
                    customer_name=customer_name,
                    customer_email=customer_email,
                    customer_phone=customer_phone,
                    event_type=event_type,
                    reservation_date=reservation_datetime,
                    number_of_guests=int(number_of_guests),
                    special_requests=special_requests
                )
                messages.success(request, 'Reservation request submitted! We will confirm shortly.')
                return redirect('make_reservation')
            except Exception as e:
                messages.error(request, 'Invalid date/time format. Please try again.')
    
    context = {
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/reservation.html", context)


def signup_view(request):
    """User registration/signup"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        
        if not all([username, email, password, password_confirm]):
            messages.error(request, 'Please fill in all required fields.')
        elif password != password_confirm:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use another email or login.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            login(request, user)
            return redirect('home')
    
    context = {
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/signup.html", context)


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not all([username, password]):
            messages.error(request, 'Please enter both username and password.')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    
    context = {
        'cart_count': get_cart_count(request),
    }
    return render(request, "menu/login.html", context)


@login_required
def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')
