from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:coffee_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:coffee_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:coffee_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/discount/', views.apply_discount_code, name='apply_discount'),
    path('order/place/', views.place_order, name='place_order'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order/track/<int:order_id>/', views.track_order, name='track_order'),
    path('order/<int:order_id>/feedback/', views.submit_feedback, name='submit_feedback'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('feedbacks/', views.view_feedbacks, name='view_feedbacks'),
    # Business pages
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),
    path('location/', views.location_hours, name='location_hours'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('offers/', views.special_offers, name='special_offers'),
    path('gallery/', views.gallery, name='gallery'),
    path('faq/', views.faq, name='faq'),
    path('reservation/', views.make_reservation, name='make_reservation'),
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
