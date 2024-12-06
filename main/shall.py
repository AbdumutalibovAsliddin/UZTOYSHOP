from .models import ProductColor, Color

# Ranglar ro'yxatini olish
colors = set(ProductColor.objects.values_list('color', flat=True))

# Ranglarni yangi Color modeliga qo'shish
for color_name in colors:
    Color.objects.get_or_create(name=color_name)

# Endi ProductColor yozuvlarini yangilash
# Ranglarni yangi Color obyektlariga bog'lash
for product_color in ProductColor.objects.all():
    try:
        color_obj = Color.objects.get(name=product_color.color)
        product_color.color = color_obj  # ProductColor modelidagi color maydonini yangilang
        product_color.save()
    except Color.DoesNotExist:
        print(f"Rang topilmadi: {product_color.color}")  # Rang topilmasa xatolikni chiqarish
