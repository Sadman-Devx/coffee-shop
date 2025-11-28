from django.core.management.base import BaseCommand
from menu.models import Coffee


class Command(BaseCommand):
    help = 'Populate database with initial coffee items'

    def handle(self, *args, **options):
        coffees_data = [
            {
                "name": "Velvet Espresso",
                "price": 4.50,
                "origin": "Ethiopian Yirgacheffe",
                "strength": "Bold & Syrupy",
                "notes": "Dark chocolate, caramel, hint of citrus",
                "image": "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=600&h=600&fit=crop",
            },
            {
                "name": "Honeycomb Latte",
                "price": 5.00,
                "origin": "Costa Rican Tarrazú",
                "strength": "Silky & Balanced",
                "notes": "Honey drizzle, steamed oat milk, vanilla foam",
                "image": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=600&h=600&fit=crop",
            },
            {
                "name": "Cocoa Cold Brew",
                "price": 5.50,
                "origin": "Colombian Supremo",
                "strength": "Chilled & Smooth",
                "notes": "24-hour steep, cacao nibs, orange zest",
                "image": "https://images.unsplash.com/photo-1517487881594-2787fef5ebf7?w=600&h=600&fit=crop",
            },
            {
                "name": "Cascara Tonic",
                "price": 4.25,
                "origin": "Guatemalan Antigua",
                "strength": "Sparkling & Bright",
                "notes": "Cascara syrup, tonic water, grapefruit peel",
                "image": "https://images.unsplash.com/photo-1517487881594-2787fef5ebf7?w=600&h=600&fit=crop",
            },
            {
                "name": "Maple Cardamom Cappuccino",
                "price": 5.25,
                "origin": "Brazilian Cerrado",
                "strength": "Creamy & Comforting",
                "notes": "Microfoam, toasted cardamom, maple sugar",
                "image": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=600&h=600&fit=crop",
            },
            {
                "name": "Nitro Midnight Mocha",
                "price": 5.75,
                "origin": "Sumatran Mandheling",
                "strength": "Velvety & Indulgent",
                "notes": "Nitro pour, dark cocoa, smoked sea salt",
                "image": "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=600&h=600&fit=crop",
            },
        ]

        created_count = 0
        for coffee_data in coffees_data:
            coffee, created = Coffee.objects.get_or_create(
                name=coffee_data["name"],
                defaults=coffee_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {coffee.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Already exists: {coffee.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully populated {created_count} coffee items!')
        )

