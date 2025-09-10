# from django.test import TestCase
# from django.urls import reverse
# from main.models import Product
# from django.contrib.auth import get_user_model
# from users.models import Seller  # <-- импортируем Selle
# User = get_user_model()

# class SimpleTestCase(TestCase):
#     def test_homepage_status_code(self):
#         """Проверка, что главная страница возвращает код 200"""
#         url = reverse('choose_role')  # Заменить на реальное имя URL
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)

# class ProductModelTest(TestCase):
#     def test_product_creation(self):
#         seller = Seller.objects.create(name="SellerName")  # создаём продавца
#         product = Product.objects.create(
#             name="Телефон",
#             price=500,
#             seller=seller
#         )
#         self.assertEqual(product.name, "Телефон")
#         self.assertEqual(product.price, 500)
#         self.assertEqual(product.seller, seller)