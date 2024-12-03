from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


from Shop3DModels.viewmodels.categories_viewmodel import CatalogViewModel
from Shop3DModels.viewmodels.products_viewmodel import ProductViewModel


class HomeView(TemplateView):
    template_name = 'home.html'


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


class ProductDetailView(TemplateView):
    template_name = 'product_detail.html'


class CartView(TemplateView):
    template_name = 'user_card.html'


class CheckoutView(TemplateView):
    template_name = 'checkout.html'


class UserProfileView(TemplateView):
    template_name = 'user_profile.html'


class AboutUsView(TemplateView):
    template_name = 'about_us.html'


class ContactUsView(TemplateView):
    template_name = 'contact_us.html'


class AdminPanelView(TemplateView):
    template_name = 'admin_panel.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'
