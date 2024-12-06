import re
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from account.models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfile, UserProfileRegisterForm, LoginForm , ProductForm, ImageFormSet, ProductColorFormSet
#CREATE PRODUCT FORM
from .forms import CreateImageFormSet,CreateProductColorFormSet,CreateProductForm
from main.models import Product, Contact, ProductColor
from .models import SoldProduct
from cart.models import Order
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import timedelta, date, datetime
from django.db.models import Sum, F, Q

# Create your views here.
@login_required
def dashboard_home(request):
    if request.user.role == "admin":
        monthly_profit_or_loss = []

        for month in range(1, 13):  # 1 dan 12 gacha (yanvardan dekabrgacha)
            # Buyurtmalarni filtrlash: oyni va statusni tekshirish
            if request.GET.get('year'):
                year = request.GET.get('year')
            else:
                year = datetime.now().year
            orders = Order.objects.filter(status="S", date__month=month,date__year=year)
            sold_product =  SoldProduct.objects.filter(sale_date__month=month,sale_date__year=year)
            # Foyda yoki zararni hisoblash
            total_profit_or_loss = orders.aggregate(
                total_profit_or_loss=Sum(
                    (F('items__product__final_price') - F('items__product__original_price')) * F('items__quantity')
                )
            )['total_profit_or_loss']
            offline_profit_or_loss = sold_product.aggregate(
                offline_profit_or_loss=Sum(
                    (F('product__final_price') - F('product__original_price')) * F('sold_quantity')
                )
            )['offline_profit_or_loss']
            total_profit_or_loss = total_profit_or_loss if total_profit_or_loss else 0
            offline_profit_or_loss = offline_profit_or_loss if offline_profit_or_loss else 0
            monthly_profit_or_loss.append(total_profit_or_loss+offline_profit_or_loss)
        data = {
            'monthly_profit_or_loss':monthly_profit_or_loss,
            'now_month_profit': "{:,}".format(monthly_profit_or_loss[datetime.now().month-1]),
            'now_year_profit': "{:,}".format(sum(monthly_profit_or_loss)),
            'contact_count': Contact.objects.count(),
            'costumers_count': UserProfile.objects.filter(role="client").count(),
            'total_price': sum(
                product.final_price * product.get_product_quantity()
                for product in Product.objects.prefetch_related('colors')
            ),
            'total_orginal_price': sum(
                product.original_price * product.get_product_quantity()
                for product in Product.objects.prefetch_related('colors')
            ),
            'years': list(range(2024, datetime.now().year  + 1))
        }
        data['net_profit'] = data['total_price'] - data['total_orginal_price']
        return render(request,'dashboard/index.html',data) 
    elif request.user.role == "seller":
        return redirect('dashboard:product_list')
    else:
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('main:home')
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = re.sub(r'\D', '',form.cleaned_data.get('phone_number'))
            password = form.cleaned_data.get('password')
            user = authenticate(request, phone_number=phone_number, password=password)

            if user is not None:
                if user.role not in ["seller", "admin"]:
                    messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
                    return redirect('main:home')
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {user.first_name}!")
                return redirect('dashboard:home')  # Muvaffaqiyatli login qilinganidan keyin yo'naltiriladigan sahifa
            else:
                messages.error(request, "Telefon raqami yoki parol noto‘g‘ri.")
        else:
            messages.error(request, "Iltimos, shaklni to'g'ri to'ldiring.")
    else:
        form = LoginForm()
    
    return render(request, 'dashboard/login.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == "POST":  # Faqat POST so'rovini qabul qilamiz
        logout(request)  # Foydalanuvchini tizimdan chiqaring
        return redirect('dashboard:login')  # Chiqishdan so'ng bosh sahifaga yo'naltirish
    else:
        # GET so'rovini rad etish
        return redirect('dashboard:home') 
@login_required
def profile_view(request):
    if request.user.role not in ["seller", "admin"]:
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('main:home')
    if request.GET.get('id'):
        try:
            user_profile = UserProfile.objects.get(id=request.GET.get('id'), role__in=["seller", "admin"])
        except:
            return redirect('dashboard:home')
        print(user_profile)
    else:
        user_profile = request.user  # Agar foydalanuvchi tizimga kirgan bo'lsa, uning profili olinadi
    return render(request, 'dashboard/adminprofile.html', {'user_profile': user_profile})
@login_required
def edit_profile(request):
    if request.user.role not in ["seller", "admin"]:
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('main:home')
    if request.method == 'POST':
        form = UpdateProfile(request.POST, request.FILES, instance=request.user)
        print(request.POST)  # POST ma'lumotlarini chiqarish
        if form.is_valid():
            print(form.cleaned_data)  # Valid formani tekshirish
            form.save()
            messages.success(request, 'Profilingiz muvaffaqiyatli yangilandi!')
            return redirect(f"{reverse('dashboard:profile')}")
        else:
            print(form.errors)  # Xatoliklarni chiqarish
    else:
        form = UpdateProfile(instance=request.user)
    return render(request,'dashboard/adminprofileedit.html', {'form': form})
def register(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['phone_number'] = re.sub(r'\D', '', post_data.get('phone_number', ''))
        form = UserProfileRegisterForm(post_data, request.FILES)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            print(phone_number)
            # Foydalanuvchini yaratish
            user_profile = form.save(commit=False)
            user_profile.role = "seller"
            user_profile.set_password(form.cleaned_data['password'])  # Parolni o'rnatish
            user_profile.save()

            # Foydalanuvchini tizimga kiritish
            login(request, user_profile)

            messages.success(request, 'Ro\'yxatdan o\'tdingiz va tizimga kiritildingiz!')
            return redirect('dashboard:home')  # Bu yerda home sahifangizni yo'naltirish
        else:
            # Agar formda xatolik bo'lsa, xatoliklarni chiqarish
            print(form.errors)
    else:
        form = UserProfileRegisterForm()

    return render(request, 'dashboard/register.html', {'form': form})
@login_required
def product_list(request):
    if request.user.role not in ["seller", "admin"]:
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('main:home')
    if request.user.role == "admin":
        products = Product.objects.all()
        if request.GET.get('q'):
            query = request.GET.get('q')
            products = products.filter(
            Q(name__icontains=query) |       # Mahsulot nomida qidiruv
            Q(description__icontains=query) |  # Tavsifda qidiruv
            Q(brend__name__icontains=query)    # Brend nomida qidiruv
        ).distinct() 
    elif request.user.role == "seller":
        user = request.user
        products = Product.objects.filter(seller=user)
        if request.GET.get('q'):
            query = request.GET.get('q')
            products = products.filter(
            Q(name__icontains=query) |       # Mahsulot nomida qidiruv
            Q(description__icontains=query) |  # Tavsifda qidiruv
            Q(brend__name__icontains=query)    # Brend nomida qidiruv
        ).distinct() 
    # Templatega ma'lumotlarni yuborish
    return render(request, 'dashboard/tables.html', {'products': products})
@login_required
def edit_product(request, product_id):
    if request.user.role not in ["seller", "admin"]:
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('main:home')
    if request.user.role == "admin":
        product = get_object_or_404(Product, id=product_id)
    elif request.user.role == "seller":
        product = get_object_or_404(Product, id=product_id)
        if product.seller != request.user:
            messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
            return redirect('dashboard:product_list')
    
    if request.method == 'POST':
        # Formalar va formsetlar
        product_form = ProductForm(request.POST, instance=product)
        image_formset = ImageFormSet(request.POST, request.FILES, instance=product)
        color_formset = ProductColorFormSet(request.POST, instance=product)

        # Product formasi tekshiruvi
        if product_form.is_valid():
            product_form.save()
        else:
            print("Product form xatoliklari:", product_form.errors)

        # Image formset tekshiruvi
        if image_formset.is_valid():
            images = image_formset.save(commit=False)
            for image in images:
                image.product = product
                image.save()
            for image in image_formset.deleted_objects:
                image.delete()
        else:
            print("Image formasi xatoliklari:", image_formset.errors)


        # Color formset tekshiruvi
        if color_formset.is_valid() or color_formset.errors == []:
            print(request.POST)
            color_formset.save()
        else:
            print("Color formasi bo'sh yoki noto'g'ri:", color_formset.errors)

        # Agar barcha formalar va formsetlar to'g'ri bo'lsa, saqlash
        if product_form.is_valid() and image_formset.is_valid() and color_formset.is_valid():
            messages.success(request, "Amal muvaffaqiyatli bajarildi!")
            return redirect('dashboard:product_list')
        else:
            product_form = ProductForm(instance=product)
            image_formset = ImageFormSet(instance=product)
            color_formset = ProductColorFormSet(instance=product) 
    else:
        # Formalarni boshidan yuklash
        product_form = ProductForm(instance=product)
        image_formset = ImageFormSet(instance=product)
        color_formset = ProductColorFormSet(instance=product)

    return render(request, 'dashboard/productedit.html', {
        'product': product,
        'product_form': product_form,
        'image_formset': image_formset,
        'color_formset': color_formset
    })
@login_required
def product_create(request):
    if request.user.role not in ["seller", "admin"]:
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('main:home')
    if request.method == 'POST':
        form = CreateProductForm(request.POST)
        color_formset = CreateProductColorFormSet(request.POST)
        image_formset = CreateImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and color_formset.is_valid() and image_formset.is_valid():
            # Formni commit=False yordamida saqlash
            product = form.save(commit=False, user=request.user)
            product.save()  # commit=True bilan saqlash
            form.save_m2m()
            
            # Formsetlarni product bilan bog'lash va saqlash
            color_formset.instance = product
            image_formset.instance = product
            color_formset.save()
            image_formset.save()

            print("Mahsulot yaratildi: ", product)
            return redirect('dashboard:product_list')
        else:
            print("Formada xatoliklar:", form.errors)
            print("Rang formasi xatoliklari:", color_formset.errors)
            print("Rasm formasi xatoliklari:", image_formset.errors)
    else:
        form = CreateProductForm()
        color_formset = CreateProductColorFormSet()
        image_formset = CreateImageFormSet()

    context = {
        'form': form,
        'color_formset': color_formset,
        'image_formset': image_formset,
    }
    return render(request, 'dashboard/product_create.html', context)

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'dashboard/product_confirm_delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('dashboard:product_list')  # Mahsulotlar ro'yxatiga yo'naltirish

    def dispatch(self, request, *args, **kwargs):
        # Mahsulotni olish
        product = self.get_object()

        # Foydalanuvchi roli tekshiriladi
        if request.user.role not in ["admin", "seller"]:
            messages.error(request, "Kechirasiz, bu sahifaga kirishga ruxsat yo'q!")
            return redirect('dashboard:product_list')  # Ruxsat berilmagan foydalanuvchini qaytarish

        # Agar seller bo'lsa, faqat o'z mahsulotini o'chirishi mumkin
        if request.user.role == "seller" and product.seller != request.user:
            messages.error(request, "Siz faqat o'zingizga tegishli mahsulotlarni o'chirishingiz mumkin!")
            return redirect('dashboard:product_list')

        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        messages.success(self.request, 'Mahsulot muvaffaqiyatli o\'chirildi!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Xatolik yuz berdi.')
        return super().form_invalid(form)

@login_required
def barcode_view(request):
    if request.user.role not in ["seller", "admin"]:
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('main:home')
    return render(request,'dashboard/barcode.html')

@login_required
def barcode_detail_view(request,barcode):
    if request.user.role not in ["seller", "admin"]:
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('main:home')
    if Product.objects.filter(barcode=barcode).exists():
        product = Product.objects.get(barcode=barcode)
        if request.method == 'POST':
            quantity = request.POST.get('quantity')
            product_color = ProductColor.objects.get(id=request.POST.get('color'))
            total_price = int(product_color.product.final_price) * int(quantity)
            
            if int(product_color.stock_quantity) < int(quantity):
                messages.error(request,"Mahsulot Bazada Yetarlik Emas!")
                return redirect('dashboard:barcode_detail',barcode=barcode)
            else:
                sold_product = SoldProduct.objects.create(
                    product=product_color.product,
                    product_color=product_color,
                    sold_quantity=quantity,
                    total_price=total_price,
                    seller=request.user,
                )
                product_color.stock_quantity = product_color.stock_quantity - int(quantity)
                product_color.save()
                messages.success(request,'Mahsulot Bazadan Ayrildi!')
        data = {
            'product': product
        }

        return render(request,'dashboard/product_barcode.html',data)
    else:
        messages.success(request,"Bunday Mahsulot Topilmadi")
        return redirect('dashboard:barcode_view')
    
@login_required
def contact_view(request):
    if request.user.role not in ["seller", "admin"]:
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('main:home')
    data = {
        'contacts': Contact.objects.all().order_by('-id')
    }
    return render(request,'dashboard/contacts.html',data)

@login_required
def message_detail(request, message_id):
    if request.user.role not in ["seller", "admin"]:
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('main:home')
    # Fetch the message by ID or return a 404 error if it doesn't exist
    message = get_object_or_404(Contact, id=message_id)
    
    # Pass the message object to the template
    return render(request, 'dashboard/message.html', {'message': message})

@login_required
def orders_view(request):
    if request.user.role not in ["seller", "admin"]:
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('main:home')
    today = date.today()
    one_month_ago = today - timedelta(days=30)

    new_orders = Order.objects.filter(created_at__gte=one_month_ago).order_by('-created_at')  # So'nggi 1 oylik yangi buyurtmalar
    canceled_orders = Order.objects.filter(status="F").order_by('-id')  # Bekor qilinganlar
    old_orders = Order.objects.exclude(status__in="F",created_at__gte=one_month_ago).order_by('-id')  # Eski buyurtmalar

    data = {
        'orders': new_orders,
        'canceled_orders': canceled_orders,
        'old_orders': old_orders,
    }
    return render(request, 'dashboard/orders.html', data)

@login_required
def order_detail(request,pk):
    if request.user.role not in ["seller", "admin"]:
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('main:home')
    order = Order.objects.get(id=pk)
    data = {
        'order':order
    }
    return render(request,'dashboard/orderview.html',data)
def seller_view(request):
    if request.user.role not in ["seller", "admin"]:
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('main:home')
    elif request.user.role == "seller":
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('dashboard:product_list')
    data = {
        'boss': UserProfile.objects.filter(role="admin",is_superuser=True).first(),
        'sellers': UserProfile.objects.filter(role__in=['seller','admin']).exclude(id=UserProfile.objects.filter(role="admin",is_superuser=True).first().id)
    }
    return render(request,'dashboard/all-seller.html',data)
@csrf_exempt
def edit_order_status(request):
    if request.user.role not in ["seller", "admin"]:
        messages.error(request, "Kechirasiz sizda bu sahifaga kirishga ruxsat yo'q!")
        return redirect('main:home')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON formatida kelgan ma'lumotni o'qish
            order_id = data.get('order_id')  # Order ID
            status = data.get('status')  # Sana (YYYY-MM-DD formatida)

            # Sana va ID ni tekshirish
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            return JsonResponse({"status": "success", "message": "Order date updated successfully"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method"})
class UserProfileDeleteView(DeleteView):
    model = UserProfile
    template_name = 'dashboard/userprofile_confirm_delete.html'
    context_object_name = 'seller'
    success_url = reverse_lazy('dashboard:seller_view')

    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in ["admin"]:
            messages.error(request, "Kechirasiz, bu sahifaga kirishga ruxsat yo'q!")
            return redirect('dashboard:product_list')  # Ruxsat berilmagan foydalanuvchini qaytarish
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        messages.success(self.request, 'Sotuvchi muvaffaqiyatli o\'chirildi!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Xatolik yuz berdi.')
        return super().form_invalid(form)
    
def total_order(request):
    monthly_profit_or_loss = []

    for month in range(1, 13):  # 1 dan 12 gacha (yanvardan dekabrgacha)
        # Buyurtmalarni filtrlash: oyni va statusni tekshirish
        orders = Order.objects.filter(status="S", date__month=month)
        
        # Foyda yoki zararni hisoblash
        total_profit_or_loss = orders.aggregate(
            total_profit_or_loss=Sum(
                (F('items__product__final_price') - F('items__product__original_price')) * F('items__quantity')
            )
        )['total_profit_or_loss']
        
        # Natijani ro'yxatga qo'shish, agar total_profit_or_loss None bo'lsa 0 qilib qo'yish
        monthly_profit_or_loss.append(total_profit_or_loss if total_profit_or_loss else 0)
    return JsonResponse({"price":monthly_profit_or_loss})