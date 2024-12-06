from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserProfileManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Telefon raqami bo'sh bo'lishi mumkin emas.")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone_number, password, **extra_fields)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    last_name = models.CharField(max_length=100, verbose_name="Last Name",blank=True,null=True)
    first_name = models.CharField(max_length=100, verbose_name="First Name",blank=True,null=True)
    address = models.CharField(max_length=255, verbose_name="Address",blank=True,null=True)
    telegram_id = models.PositiveIntegerField(default=0,blank=True,null=True)

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    ROLE_CHOICES = (
        ('admin','Admin'),
        ('seller','Seller'),
        ('client','Client')
    )
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, verbose_name='Role', default='client', blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name="Gender",blank=True,null=True)
    
    email = models.EmailField(verbose_name="Email", unique=True,blank=True,null=True)
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Phone Number",blank=True,null=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)  # SMS tasdiqlash kodi
    is_verified = models.BooleanField(default=False)  # Tasdiqlash holati
    is_active = models.BooleanField(default=True)  # Foydalanuvchi faolligi
    is_staff = models.BooleanField(default=False)  # Admin panelga kirish
    picture = models.ImageField(upload_to="user_pictures/",blank=True,null=True)

    USERNAME_FIELD = 'phone_number'  # Foydalanuvchining foydalanuvchi nomi sifatida telefon raqami
    # REQUIRED_FIELDS = ['last_name', 'first_name', 'email']  # Qo'shimcha talab qilinadigan maydonlar

    objects = UserProfileManager()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    def get_format_phone(self):
        phone_number = self.phone_number
        return f"+998 {phone_number[3:5]} {phone_number[5:8]} {phone_number[8:10]} {phone_number[10:]}"
    def get_seller_product(self):
        return self.products.count()
    def get_seller_order(self):
        order_count = sum(product.order_count for product in self.products.all())
        return order_count if order_count else 0