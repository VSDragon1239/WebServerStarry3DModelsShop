from django.contrib import admin
from .models import Category, Product, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')  # Поля для отображения
    search_fields = ('name',)  # Поля для поиска


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'is_active')
    list_filter = ('category', 'is_active')  # Фильтрация
    search_fields = ('name', 'description')  # Поля для поиска


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'delivery_address')
    list_filter = ('status',)  # Фильтрация по статусу
    search_fields = ('user__username', 'delivery_address')
