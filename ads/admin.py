from django.contrib import admin
from .models import Cat, Breed, SellerProfile

admin.site.register(Cat)
admin.site.register(Breed)
admin.site.register(SellerProfile)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        SellerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.sellerprofile.save()
