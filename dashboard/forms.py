import re
from django import forms
from django.forms.models import inlineformset_factory
from account.models import UserProfile
from main.models import Product, Image, ProductColor, Rating

class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UpdateProfile(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'picture','telegram_id']
class UserProfileRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    # Telefon raqamiga faqat raqamlarni kiritish va 15 ta belgi bilan cheklash
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number', 'email']
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        
        # Raqamlar tashqari barcha belgilarni olib tashlash
        phone_number = re.sub(r'\D', '', phone_number)
        
        # Telefon raqamini tekshirish: 15 ta belgidan oshmasligi kerak
        if len(phone_number) > 15:
            raise forms.ValidationError("Telefon raqami 15 belgidan oshmasligi kerak.")
        
        return phone_number
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError("Parollar mos kelmadi.")
        
        return cleaned_data
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'final_price','description' ,'discount', 'category', 'brend', 'show_product']
        
ImageFormSet = inlineformset_factory(Product, Image, fields=['image','product'], extra=1, can_delete=True)
ProductColorFormSet = inlineformset_factory(Product, ProductColor, fields=['color', 'stock_quantity'], extra=1, can_delete=True)

# PRODUCT CREATE FORM
class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'discount', 'category', 'brend', 'show_product']
    

    def save(self, commit=True, user=None):
        # commit=False yordamida obyektni yarating
        product = super().save(commit=False)
        if user:
            product.seller = user  # request.user ni seller maydoniga tenglash
        if commit:
            product.save()  # Obyektni saqlash
        return product


CreateProductColorFormSet = inlineformset_factory(
    Product,
    ProductColor,
    fields=['color', 'stock_quantity'],
    extra=1,
    can_delete=True
    
)

CreateImageFormSet = inlineformset_factory(
    Product,
    Image,
    fields=['image'],
    extra=1,
    can_delete=True
)