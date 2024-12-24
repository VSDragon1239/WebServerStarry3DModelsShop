from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", blank=True)
    slug = models.SlugField(verbose_name="Slug", max_length=150, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тег", unique=True)
    slug = models.SlugField(verbose_name="Slug", max_length=150, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    tags = models.ManyToManyField(Tag, verbose_name="Теги", blank=True, related_name="products")
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2)
    description = models.TextField(verbose_name="Описание", blank=True)
    dimensions = models.CharField(max_length=255, verbose_name="Размеры", blank=True)
    compatibility = models.CharField(max_length=255, verbose_name="Совместимость с принтерами", blank=True)
    materials = models.CharField(max_length=255, verbose_name="Материалы", blank=True)
    image = models.ImageField(upload_to="products/images", verbose_name="Изображение", blank=True, null=True)
    model_files = models.FileField(upload_to="products/models", verbose_name="Файлы модели (STL/OBJ и др.)", blank=True, null=True)
    rating = models.FloatField(verbose_name="Рейтинг", default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт", related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.PositiveSmallIntegerField(verbose_name="Рейтинг", default=5)
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв на {self.product.name} от {self.user.username}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", blank=True, null=True)
    session_key = models.CharField(max_length=40, verbose_name="Сессионный ключ", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина {self.user.username if self.user else 'Гостя'}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина", related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=1)

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

    def __str__(self):
        return f"{self.quantity} x {self.product.name} в корзине {self.cart.user.username if self.cart.user else 'Гостя'}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    total_price = models.DecimalField(verbose_name="Общая стоимость", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    status = models.CharField(
        max_length=50,
        verbose_name="Статус заказа",
        choices=[("pending", "В ожидании"), ("completed", "Завершён"), ("canceled", "Отменён")],
        default="pending",
    )
    delivery_address = models.TextField(verbose_name="Адрес доставки")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id} ({self.user.username})"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные модели"

    def __str__(self):
        return f"Избранное: {self.product.name} ({self.user.username})"
