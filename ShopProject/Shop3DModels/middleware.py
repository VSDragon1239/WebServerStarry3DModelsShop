from Shop3DModels.models import Cart


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            cart = Cart.objects.filter(session_key=session_key).first() if session_key else None

        request.session['cart_count'] = sum(item.quantity for item in cart.items.all()) if cart else 0
        return self.get_response(request)
