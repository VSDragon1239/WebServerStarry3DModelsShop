from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart
from .views import MergeGuestCartView


@receiver(user_logged_in)
def merge_guest_cart(sender, request, user, **kwargs):
    session_key = request.session.session_key
    if session_key:
        MergeGuestCartView().merge_carts(user, session_key)
