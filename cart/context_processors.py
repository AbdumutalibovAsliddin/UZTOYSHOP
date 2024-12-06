from .models import Cart, CartItem
from .views import get_or_create_cart

def cart_count(request):
    # Savatdagi mahsulotlar sonini hisoblash
    cart_count = 0
    if request.user.is_authenticated:
        try:
            # Foydalanuvchi uchun savatni olish
            cart = get_or_create_cart(request)
            cart_count = cart.items.count()
        except Cart.DoesNotExist:
            pass
    return {'cart_count': cart_count}
