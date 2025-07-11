from django.core.management.base import BaseCommand
from cat_ads.models import CatAd

class Command(BaseCommand):
    help = 'Resizes existing images'

    def handle(self, *args, **options):
        for cat_ad in CatAd.objects.all():
            print(f"Resizing image for {cat_ad.title}")
            cat_ad.save()  # Вызываем метод save(), который изменит размер
        self.stdout.write(self.style.SUCCESS('Successfully resized all images'))