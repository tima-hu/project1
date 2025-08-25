from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# =====================
#   КАСТОМНЫЙ ПОЛЬЗОВАТЕЛЬ
# =====================
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


# =====================
#   ПРОФИЛЬ ПРОДАВЦА
# =====================
class Seller(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller"
    )
    store_name = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.store_name or f"Магазин {self.user.username}"


# =====================
#   ЧАТ
# =====================
class ChatMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_messages"
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:30]}"


# =====================
#   ТОВАРЫ
# =====================
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Электроника'),
        ('clothes', 'Одежда'),
        ('toys', 'Игрушки'),
        ('home', 'Товары для дома'),
        ('other', 'Прочее'),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, verbose_name="Категория")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    seller = models.ForeignKey("Seller", on_delete=models.CASCADE, related_name="products")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"


# =====================
#   КОРЗИНА И ЗАКАЗЫ
# =====================
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart #{self.id} for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='processing')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


# =====================
#   СИГНАЛ ДЛЯ СОЗДАНИЯ ПРОДАВЦА
# =====================
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_seller_for_new_user(sender, instance, created, **kwargs):
    """Автоматически создаём профиль продавца для всех пользователей"""
    if created:
        Seller.objects.get_or_create(
            user=instance,
            defaults={"store_name": f"Магазин {instance.username}"}
        )
