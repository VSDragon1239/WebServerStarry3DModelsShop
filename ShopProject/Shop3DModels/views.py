from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView

from Shop3DModels.viewmodels.categories_viewmodel import CatalogViewModel
from Shop3DModels.viewmodels.products_viewmodel import ProductViewModel

from Shop3DModels.models import Cart, CartItem, Product, Order

from Shop3DModels.forms import CustomUserCreationForm


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Динамически загружаем последние 8 товаров
        context['products'] = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
        return context


class CatalogView(TemplateView):
    template_name = 'catalog.html'

    CatalogView = []
    categories = []
    filters_array = []

    def get(self, request, *args, **kwargs):
        self.initViewModel()
        self.filters_array = request.GET.get('filters', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.initViewModel()
        context = super().get_context_data(**kwargs)
        context["categories"] = self.categories
        return context

    def initViewModel(self):
        self.CatalogView = CatalogViewModel()
        self.categories = self.CatalogView.get_categories()


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class CartView(TemplateView):
    template_name = 'user_cart.html'

    def get(self, request, *args, **kwargs):
        self.cart = self.get_cart(request)
        self.items = self.cart.items.all()
        self.total_price = sum(item.product.price * item.quantity for item in self.items)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.items
        context['total_price'] = self.total_price
        return context

    def get_cart(self, request):
        """Получение текущей корзины"""
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
            cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
        return cart


class AddToCartView(TemplateView):
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        cart = CartView().get_cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return JsonResponse({'status': 'success', 'message': 'Товар добавлен в корзину'})


class UpdateCartItemView(TemplateView):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        cart = CartView().get_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
        return JsonResponse({'status': 'success', 'message': 'Количество обновлено'})


class RemoveFromCartView(TemplateView):
    def post(self, request, *args, **kwargs):
        item_id = kwargs.get('item_id')
        cart = CartView().get_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return JsonResponse({'status': 'success', 'message': 'Товар удален из корзины'})


class MergeGuestCartView(TemplateView):
    """Объединение гостевой корзины с пользовательской при входе"""
    def merge_carts(self, user, session_key):
        guest_cart = Cart.objects.filter(session_key=session_key).first()
        if guest_cart:
            user_cart, _ = Cart.objects.get_or_create(user=user)
            for item in guest_cart.items.all():
                user_item, created = CartItem.objects.get_or_create(cart=user_cart, product=item.product)
                if not created:
                    user_item.quantity += item.quantity
                user_item.save()
            guest_cart.delete()


class CheckoutView(TemplateView):
    template_name = 'checkout.html'

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return redirect('card')

        # Создание заказа
        total_price = sum(item.product.price * item.quantity for item in cart.items.all())
        Order.objects.create(
            user=request.user,
            total_price=total_price,
            delivery_address=request.POST.get('delivery_address', ''),
        )

        # Очистка корзины
        cart.items.all().delete()

        return redirect('user_profile')


class UserProfileView(TemplateView):
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user)
        return context


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        # Перенаправление на предыдущую страницу, если задана, или на главную
        return self.request.GET.get('next', reverse_lazy('home'))


class CustomLogoutView(LogoutView):
    template_name = 'logout.html'

    def dispatch(self, request, *args, **kwargs):
        # Добавляем сообщение об успешном выходе
        messages.success(request, "Вы успешно вышли из системы.")
        # Выполняем стандартный выход
        return super().dispatch(request, *args, **kwargs)

    def get_next_page(self):
        return 'home'  # Название маршрута для перенаправления


class AboutUsView(TemplateView):
    template_name = 'about_us.html'


class ContactUsView(TemplateView):
    template_name = 'contact_us.html'


class AdminPanelView(TemplateView):
    template_name = 'admin_panel.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'
