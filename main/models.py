from django.db import models
from account.models import UserProfile
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.timesince import timesince
import os
#BARCODE LIBRARY
from barcode import Code128
import uuid
from io import BytesIO
from barcode.writer import ImageWriter
from django.core.files import File

def generate_barcode():
    """8 belgidan iborat noyob tasodifiy kod yaratish"""
    return str(uuid.uuid4())[:8]
# Create your models here.
class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Rang nomi
    color_code = models.CharField(max_length=50,default="black")

    def __str__(self):
        return self.name
class Banner(models.Model):
    banner_link = models.URLField()
    image = models.ImageField(upload_to='banner/')

    def __str__(self):
        return self.banner_link
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_image/')
    
    def __str__(self):
        return self.name
class Image(models.Model):
    image = models.ImageField(upload_to='product/')
    product = models.ForeignKey('Product',on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.product.name
    def delete(self, *args, **kwargs):
        # Faylni o'chirish
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)
class Brend(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextUploadingField(default=" ")
    price = models.DecimalField(max_digits=100, decimal_places=2)
    final_price = models.PositiveIntegerField(default=0,blank=True,null=True)
    original_price = models.PositiveIntegerField(default=0,blank=True,null=True) 
    discount = models.PositiveIntegerField(blank=True,null=True)
    category = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    brend = models.ForeignKey(Brend,on_delete=models.CASCADE)
    order_count = models.IntegerField(default=0)
    show_product = models.BooleanField(default=False)
    seller = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=True,null=True,related_name='products')
    barcode_image = models.ImageField(upload_to='barcodes/', blank=True, null=True)
    barcode = models.CharField(max_length=8, blank=True,null=True)

    def __str__(self):
        return f"{self.name}-{self.final_price_get()}"
    def get_true_price(self):
        try:
            print(str(self.price).replace(",", "."))
            return int(self.price)
        except:
            return 0
    def get_product_images(self):
        return self.images.all() 
    def get_discounted_price(self):
        if self.discount:
            discount_amount = (self.price * self.discount) / 100
            discounted_price = self.price - discount_amount
        else:
            discounted_price = self.price
        # Raqamni formatlash: 37410.00 -> 37 410
        return f"{int(discounted_price):,}".replace(",", " ")
    def get_banner_image(self):
        return self.images.first()
    def get_discounted_price(self):
        if self.discount:
            discount_amount = (self.price * self.discount) / 100
            discounted_price = self.price - discount_amount
        else:
            discounted_price = self.price
        # Raqamni formatlash: 37410.00 -> 37 410
        return f"{int(discounted_price):,}".replace(",", " ")
    def final_price_get(self):
        if self.discount:
            discount_amount = (self.price * self.discount) / 100
            discounted_price = self.price - discount_amount
        else:
            discounted_price = self.price
        self.final_price = discounted_price
        self.save()
        return self.final_price
    def get_format_price(self):
        return f"{int(self.price):,}".replace(",", " ")
    def get_product_quantity(self):
        return sum(color.stock_quantity for color in self.colors.all())
    def get_average_rating(self):
        ratings = self.ratings.all()  # Mahsulotning barcha retinglari
        if ratings.exists():
            average_rating = ratings.aggregate(models.Avg('rating'))['rating__avg']  # O'rtacha retingni hisoblash
            return round(average_rating)  # 1ta kasr son bilan qaytariladi (masalan, 4.5)
        return 0  # Agar hali reting bo'lmasa, 0 qaytariladi
    def sold_out(self):
        return self.colors.filter(stock_quantity=0)
    def save(self, *args, **kwargs):
        # Update final_price before saving
        if not self.barcode:  # Agar barcode hali mavjud bo'lmasa
            # Tasodifiy barcode yaratish
            barcode_value = generate_barcode()
            while Product.objects.filter(barcode=barcode_value).exists():
                barcode_value = generate_barcode()
            self.barcode = barcode_value

            # Barcode tasvirini yaratish
            ean = Code128(self.barcode, writer=ImageWriter())  # 'Code128' format
            buffer = BytesIO()  # Xotirada vaqtinchalik saqlash uchun buffer
            ean.write(buffer)  # Tasvirni bufferga yozish
            self.barcode_image.save(f'barcode-{self.barcode}.png', File(buffer), save=False)
        if self.discount:
            discount_amount = (self.price * self.discount) / 100
            discounted_price = self.price - discount_amount
        else:
            discounted_price = self.price
        self.final_price = discounted_price
        super().save(*args, **kwargs)

class ProductColor(models.Model):
    product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE)  # Har bir mahsulotga ranglar bog'lanadi
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True) # Rang nomi (masalan, "qizil", "ko'k")
    stock_quantity = models.IntegerField(default=0)  # Ushbu rangdagi mahsulot soni

    def __str__(self):
        return f'{self.color.color_code} - {self.color.name}'

    def is_in_stock(self):
        return self.stock_quantity > 0 
class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # Foydalanuvchi
    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)  # Mahsulot
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} rated {self.product.name} - {self.rating} Stars"
class Contact(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Ism')
    last_name = models.CharField(max_length=100, verbose_name='Familiya')
    phone_number = models.CharField(max_length=15, verbose_name='Telefon Raqami')
    address = models.CharField(max_length=255, verbose_name='Manzil')
    description = models.TextField(blank=True, null=True, verbose_name='Tavsif')
    create_time = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number}"
    def time_ago(self):
        """Return the time ago string for the contact's create_time."""
        return timesince(self.create_time)