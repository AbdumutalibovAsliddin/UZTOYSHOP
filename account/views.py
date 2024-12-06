from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UserProfile
from django.contrib.auth import login, logout
from django.http import JsonResponse
import json
from django.urls import reverse
from .utils import send_verification_code
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from cart.models import Order


def login_view(request):
    return redirect('/#login')

@login_required
def logout_view(request):
    logout(request)  # Foydalanuvchini tizimdan chiqish
    messages.success(request, "Siz muvaffaqiyatli tizimdan chiqdiz!")  # Muvaffaqiyatli xabar
    return redirect('main:home')
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilingiz muvaffaqiyatli yangilandi!')
            return redirect(f"{reverse('account:profile')}#profile")  # Profil sahifasiga qaytarish
    else:
        form = UserProfileForm(instance=request.user)
    order = Order.objects.filter(user=request.user).order_by('-id')
    context = {
        'form': form,
        'orders':order,
        'new_order':order.exclude(status__in=["F", "S"]),
    }
    return render(request, 'profileandorder.html', context)
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)  # JSON formatidagi body ma'lumotlarini o'qish
        phone_number = data.get("phone_number")
        print(phone_number)
        # Foydalanuvchi ma'lumotlarini saqlash
        print(UserProfile.objects.filter(phone_number=phone_number))
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            user = UserProfile.objects.get(phone_number=phone_number)
        else:
            user = UserProfile.objects.create(
                phone_number=phone_number,
            )
        # SMS yuborish
        code = send_verification_code(phone_number)
        user.verification_code = code
        user.save()

        return JsonResponse({'user_id':user.id})# Tasdiqlash sahifasiga o'tish

    return render(request, 'home.html')

def verify(request, user_id):
    user = UserProfile.objects.get(id=user_id)
    
    if request.method == "POST":
        data = json.loads(request.body)  # JSON formatidagi body ma'lumotlarini o'qish
        input_code = data.get("verification_code")
        print(input_code)
        if input_code == user.verification_code:
            user.is_verified = True
            user.save()
            if user is not None:
                login(request, user)
            return HttpResponse("Tasdiqlash muvaffaqiyatli amalga oshirildi!")
        else:
            return HttpResponse("Tasdiqlash kodi noto'g'ri!")

    return render(request, 'home.html', {'user': user})
