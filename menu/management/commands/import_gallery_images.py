from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path

from menu.models import GalleryImage


class Command(BaseCommand):
    help = "Import local gallery images from static/img/gallery into the GalleryImage model."

    def handle(self, *args, **options):
        base_dir = Path(settings.BASE_DIR)
        gallery_dir = base_dir / "static" / "img" / "gallery"

        if not gallery_dir.exists():
            self.stdout.write(self.style.WARNING(f"No folder found at {gallery_dir}. Create it and add images first."))
            return

        exts = {".jpg", ".jpeg", ".png", ".webp"}
        files = [p for p in gallery_dir.iterdir() if p.suffix.lower() in exts]

        if not files:
            self.stdout.write(self.style.WARNING("No image files found in static/img/gallery."))
            return

        created = 0
        updated = 0

        for idx, img_path in enumerate(sorted(files)):
            path_suffix = f"/img/gallery/{img_path.name}"
            url = settings.STATIC_URL.rstrip("/") + path_suffix
            if not url.startswith("/"):
                url = "/" + url
            title = img_path.stem.replace("_", " ").replace("-", " ").title()

            obj, was_created = GalleryImage.objects.update_or_create(
                image_url__endswith=path_suffix,
                defaults={
                    "image_url": url,
                    "title": title,
                    "description": "",
                    "category": "shop",
                    "is_featured": idx < 3,  # first few as featured
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(f"Imported gallery images. Created: {created}, Updated: {updated}.")
        )


