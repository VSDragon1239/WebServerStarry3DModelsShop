# AppName/urls.py
from django.urls import path
from Shop3DModels.views import (
    HomeView, CatalogView, ProductDetailView, CartView,
    CheckoutView, UserProfileView, AboutUsView, ContactUsView,
    AdminPanelView, PrivacyPolicyView, AddToCartView, UpdateCartItemView,
    RemoveFromCartView, RegisterView, CustomLoginView, CustomLogoutView
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Основные страницы
    path('', HomeView.as_view(), name='home'),                                                 # Главная страница
    path('categories/', CatalogView.as_view(), name='catalog'),                                # Страница категорий
    path('categories/<int:pk>/products/<int:pk2>/', ProductDetailView.as_view(), name='product'),  # Страница продукта

    # Корзина
    path('card/', CartView.as_view(), name='card'),                                            # Корзина
    path('card/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),           # Добавление товара в корзину
    path('card/update/<int:item_id>/', UpdateCartItemView.as_view(), name='update_cart_item'), # Обновление товара в корзине
    path('card/remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'), # Удаление товара из корзины

    # Оформление заказа
    path('checkout/', CheckoutView.as_view(), name='checkout'),                               # Страница оформления заказа

    # Пользователь
    path('profile/', UserProfileView.as_view(), name='user_profile'),                         # Профиль пользователя
    path('register/', RegisterView.as_view(), name='register'),                               # Регистрация
    path('login/', CustomLoginView.as_view(), name='login'),                                  # Вход
    path('logout/', CustomLogoutView.as_view(), name='logout'),                               # Выход

    # Информационные страницы
    path('about/', AboutUsView.as_view(), name='about_us'),                                   # О нас
    path('contact/', ContactUsView.as_view(), name='contact_us'),                             # Контакты
    path('adminpanel/', AdminPanelView.as_view(), name='admin_panel'),                        # Панель администратора
    path('privacypolicy/', PrivacyPolicyView.as_view(), name='privacy_policy'),               # Политика конфиденциальности
]
