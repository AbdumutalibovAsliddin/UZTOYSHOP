from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from datetime import timedelta
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, Banner,Brend,Color,Rating,Contact
from .forms import ContactForm
# Create your views here.
def home(request):
    # Баннерлар, категориялар ва маҳсулотларни олиш
    banners = Banner.objects.all().order_by('-id')  # Ҳамма баннерларни оламиз

    # Янги маҳсулотларни фильтрлаш (сўнгги 30 кун ичида яратилган)
    last_30_days = timezone.now() - timedelta(days=30)
    
    # Category, Brend ва рейтинг билан бирга маҳсулотларни олдиндан юклаш
    new_products = Product.objects.filter(created_at__gte=last_30_days, show_product=True) \
                                  .select_related('brend') \
                                  .prefetch_related('category', 'ratings').order_by('-id')[:12]
    
    # Қолган маҳсулотлар ҳам худди шундай усулда олинади
    products = Product.objects.filter(show_product=True)  \
                              .select_related('brend') \
                              .prefetch_related('category', 'ratings').order_by('-id')[:20]

    # Категорияларни оламиз
    categories = Category.objects.all()

    context = {
        'banners': banners,
        'categories': categories,
        'new_products': new_products,  # Янги маҳсулотлар
        'products': products,  # Қолган маҳсулотлар
    }

    return render(request, 'home.html', context)
def product_list(request):
    # Dastlab barcha mahsulotlarni olish
    products = Product.objects.all().filter(show_product=True)
    category_param = request.GET.get('category')
    color_param = request.GET.get('color')
    brend_param = request.GET.get('brend')

    if category_param and ',' in category_param:
        # Vergul bilan ajratilganlarni listga o'zgartirish
        selected_categories = category_param.split(',')
    else:
        selected_categories = request.GET.getlist('category') 
    if color_param and ',' in color_param:
        # Vergul bilan ajratilganlarni listga o'zgartirish
        selected_colors = color_param.split(',')
    else:
        selected_colors = request.GET.getlist('color') 
    if brend_param and ',' in brend_param:
        # Vergul bilan ajratilganlarni listga o'zgartirish
        selected_brands = brend_param.split(',')
    else:
        selected_brands = request.GET.getlist('brend')

    # URL parametrlardan filtrlash qiymatlarini olish
    min_price = request.GET.get('price-from')
    max_price = request.GET.get('price-to')
    sorting = request.GET.get('sorting')
    query = request.GET.get('q', '')

    if query:
        products = products.filter(
            Q(name__icontains=query) |       # Mahsulot nomida qidiruv
            Q(description__icontains=query) |  # Tavsifda qidiruv
            Q(brend__name__icontains=query)    # Brend nomida qidiruv
        ).distinct() 
    if selected_categories:
        products = products.filter(category__name__in=selected_categories).distinct()
    if min_price:
        min_price_val = int(min_price) * 1000
        products = products.filter(final_price__gte=min_price_val)

    if max_price:
        max_price_val = int(max_price) * 1000
        products = products.filter(final_price__lte=max_price_val)

    # Ranglar bo'yicha filtrlash
    if selected_colors:
        products = products.filter(colors__color__color_code__in=selected_colors).distinct()

    # Brendlar bo'yicha filtrlash
    if selected_brands:
        products = products.filter(brend__name__in=selected_brands).distinct()

    if sorting == "ko'p sotilgan":
        products = products.order_by('-order_count')  # Eng ko'p sotilgan
    elif sorting == "arzon":
        products = products.order_by('price')  # Eng arzon
    elif sorting == "qimmat":
        products = products.order_by('-price')  # Eng qimmat
    elif sorting == "yangi":
        products = products.order_by('-created_at')

    categories = Category.objects.all()
    brands = Brend.objects.all()
    colors = Color.objects.all()

    # # Pagination
    paginator = Paginator(products, 8)  # Har sahifada 10 mahsulot
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'colors': colors,
        'selected_categories': selected_categories,  # Form uchun tanlangan kategoriyalar
        'selected_min_price': min_price,      # Tanlangan minimal narx
        'selected_max_price': max_price,      # Tanlangan maksimal narx
        'selected_colors': selected_colors,             # Tanlangan ranglar
        'selected_brands': selected_brands,    
        'sorting': sorting,
    }
    
    return render(request, 'filter.html', context)
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    category = product.category.all()  # Product obyektiga tegishli kategoriyalarni olish
    related_products = Product.objects.filter(category__in=category).exclude(id=product.id).distinct()[:4]  # Mahsulotning kategoriyasiga mos mahsulotlarni olish, hozirgi mahsulotni chiqarib tashlash
    random_products = Product.objects.exclude(id=product.id).exclude(id__in=related_products.values_list('id', flat=True)).distinct().order_by('?')[:4]
    try:
        user_rating = Rating.objects.get(user=request.user,product=product).rating
    except:
        user_rating = 0
    return render(request, 'detail.html', {
        'product': product,
        'related_products': related_products,
        'random_products':random_products,
        'user_rating':user_rating
    })
@csrf_exempt
def rate_product(request):
    if not request.user.is_authenticated:
        # Foydalanuvchi tizimga kirmagan bo'lsa, JSON javob qaytarish
        return JsonResponse({"success": False, "error": "Siz tizimga kirmagansiz. Reyting qo'shish uchun iltimos, tizimga kiring."}, status=401)

    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        rating_value = data.get("rating")

        try:
            product = Product.objects.get(id=product_id)

            # Reytingni yaratish yoki yangilash
            rating, created = Rating.objects.update_or_create(
                user=request.user,
                product=product,
                defaults={"rating": rating_value}
            )

            return JsonResponse({"success": True, "created": created})

        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Mahsulot topilmadi"}, status=404)

    return JsonResponse({"success": False, "error": "Noto'g'ri so'rov"}, status=400)
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            description = request.POST.get('description')
            bot_token = '8100584262:AAE8h6k7Tp6b9oBHKUmG_cv1MQDgM3Qq0xA'  # O'zingizning bot tokeningizni qo'shing
            chat_id = '8109565026'  # O'zingizning chat ID'ingizni qo'shing

            # Xabarni tayyorlash
            telegram_message = (
                f"Yangi kontakt ma'lumoti:\n"
                f"Ism: {first_name}\n"
                f"Familya: {last_name}\n"
                f"Telefon raqami: {phone_number}\n"
                f"Manzil: {address}\n"
                f"Xabar: {description}"
            )

            # Xabarni yuborish
            response = requests.post(
                f'https://api.telegram.org/bot{bot_token}/sendMessage',
                data={'chat_id': chat_id, 'text': telegram_message}
            )

            if response.status_code == 200:
                messages.success(request, 'Kontakt ma\'lumoti muvaffaqiyatli saqlandi va Telegramga yuborildi!')
            else:
                messages.error(request, 'Xabar yuborishda xatolik yuz berdi!')
            return redirect('main:contact')  # Yaratilgan kontaktlar ro'yxatiga o'tish
    else:
        form = ContactForm()
    
    return render(request, 'cantact.html', {'form': form})