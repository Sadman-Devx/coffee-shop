from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:coffee_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:coffee_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:coffee_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/place/', views.place_order, name='place_order'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/track/', views.track_orders, name='track_orders'),
    path('orders/<int:order_id>/', views.view_order, name='view_order'),
]
