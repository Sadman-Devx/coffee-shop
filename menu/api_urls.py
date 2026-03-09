from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import (
    CoffeeViewSet,
    OrderViewSet,
    ReservationViewSet,
    FeedbackViewSet,
)

router = DefaultRouter()
router.register(r"coffees", CoffeeViewSet, basename="coffee")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"reservations", ReservationViewSet, basename="reservation")
router.register(r"feedbacks", FeedbackViewSet, basename="feedback")

urlpatterns = [
    path("", include(router.urls)),
]

