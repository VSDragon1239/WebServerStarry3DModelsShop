# AppName/urls.py
from django.urls import path
from Shop3DModels.views import HomeView, CatalogView, ProductDetailView, CartView, CheckoutView, UserProfileView, AboutUsView, ContactUsView, AdminPanelView, PrivacyPolicyView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),                                                 # Главная страница
    path('categories/', CatalogView.as_view(), name='catalog'),                           # Страница категорий                     # Страница продуктов
    path('categories/<int:pk>/products/<int:pk2>', ProductDetailView.as_view(), name='product'),      # Страница продукта
    path('card/', CartView.as_view(), name='card'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('about/', AboutUsView.as_view(), name='about_us'),
    path('contact/', ContactUsView.as_view(), name='contact_us'),
    path('adminpanel/', AdminPanelView.as_view(), name='admin_panel'),
    path('pivacypolicy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
]
