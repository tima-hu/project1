from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from core.settings import AUTH_USER_MODEL
# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Покупатель'),
        ('seller', 'Продавец'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='buyer'
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.email

class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Покупатель: {self.user.username}"
    
class Seller(models.Model):
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller"
    )
    store_name = models.CharField(max_length=255, default="Магазин")

    def __str__(self):
        return self.store_name or f"Магазин {self.user.username}"

