from django.conf import settings
from django.db import models
from main.models import Product, ProductColor
from account.models import UserProfile
from django.utils import timezone

class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}'s cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE,null=True, blank=True)  # Mahsulot rangini saqlash uchun
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} ta"
    def save(self, *args, **kwargs):
        # Agar quantity stock_quantity dan katta bo'lsa, uni stock_quantity ga tenglashtirish
        if self.quantity > self.color.stock_quantity:
            self.quantity = self.color.stock_quantity
        super().save(*args, **kwargs)
class Address(models.Model):
    address_code = models.CharField(max_length=100,null=True, blank=True)
    latitude = models.CharField(max_length=100,null=True, blank=True)
    longitude = models.CharField(max_length=100,null=True, blank=True)
    
    def __str__(self):
        return f"{self.latitude} - {self.longitude}"
class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Kutish holati'),     # Kutish holati
        ('M', 'Tayorlanmoqda'),   # Yakunlangan
        ('R',"Yo'lda"),
        ('F', 'Bekor qilingan'),      # Xato
        ('S', 'Yetkazilgan'),     # Yetkazilgan
    ]

    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    created_at = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)  # Umumiy narx
    date = models.DateField(blank=True,null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

    def calculate_total(self):
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_price = total
        self.save()
        return total
    
    def get_all_categories(self):
        categories = set()  # Set orqali takrorlanishni oldini olish
        # Har bir OrderItem orqali tegishli mahsulotning kategoriyalarini olish
        for item in self.items.all():
            for category in item.product.category.all():
                categories.add(category.name)  # Har bir kategoriya nomini qo'shamiz
        return ", ".join(sorted(categories))
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())
    def get_format_price(self):
        return f"{int(self.total_price):,}".replace(",", " ")
    def get_status_display(self):
        # STATUS_CHOICES dagi qiymatga mos keladigan nomni qaytarish
        return dict(self.STATUS_CHOICES).get(self.status, "Unknown")
    def calculate_profit_or_loss(self):
        total_profit_or_loss = 0
        for item in self.items.all():
            # Mahsulotning sotilish narxidan (final_price) asl narxini (original_price) ayirish
            profit_or_loss_per_item = (item.product.final_price - item.product.original_price) * item.quantity
            total_profit_or_loss += profit_or_loss_per_item
        return total_profit_or_loss

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)  # Mahsulot soni
    price = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.price