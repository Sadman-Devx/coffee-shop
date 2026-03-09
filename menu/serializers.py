from rest_framework import serializers

from .models import Coffee, Order, OrderItem, Reservation, Feedback


class CoffeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coffee
        fields = [
            "id",
            "name",
            "price",
            "origin",
            "strength",
            "notes",
            "image",
            "available",
            "created_at",
            "updated_at",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    coffee = CoffeeSerializer(read_only=True)
    coffee_id = serializers.PrimaryKeyRelatedField(
        source="coffee", queryset=Coffee.objects.all(), write_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "coffee",
            "coffee_id",
            "quantity",
            "price",
        ]
        read_only_fields = ["order"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_name",
            "customer_email",
            "customer_phone",
            "delivery_address",
            "delivery_city",
            "delivery_postal_code",
            "status",
            "delivery_option",
            "payment_method",
            "payment_status",
            "total_amount",
            "discount_code",
            "discount_amount",
            "delivery_fee",
            "final_amount",
            "notes",
            "estimated_ready_time",
            "completion_message",
            "created_at",
            "updated_at",
            "items",
        ]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "id",
            "customer_name",
            "customer_email",
            "customer_phone",
            "event_type",
            "reservation_date",
            "number_of_guests",
            "special_requests",
            "status",
            "created_at",
            "updated_at",
        ]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            "id",
            "order",
            "customer_name",
            "customer_email",
            "rating",
            "comment",
            "created_at",
            "approved",
        ]
        read_only_fields = ["approved", "created_at"]

