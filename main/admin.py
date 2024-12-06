from django.contrib import admin
from .models import Banner, Category, Image, Brend, Product, ProductColor, Rating, Color, Contact

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  # Add extra image fields for easier adding

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1  # Add extra color fields for easier adding

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1  # Add extra rating fields for easier adding

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'brend', 'order_count', 'show_product', 'created_at')
    list_filter = ('brend', 'show_product', 'created_at')
    search_fields = ('name', 'description', 'brend__name')
    inlines = [ImageInline, ProductColorInline, RatingInline]

    quill_fields = {
        'description': {
            'theme': 'snow',  # You can choose between 'snow' and 'bubble'
            'modules': {
                'toolbar': [
                    [{'header': [1, 2, 3, False]}],
                    ['bold', 'italic', 'underline'],
                    ['link', 'image'],
                    [{'list': 'ordered'}, {'list': 'bullet'}],
                ]
            },
        }
    }

    # Override get_form method to include admin_params for QuillField
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if hasattr(form, 'quill_fields'):
            form.quill_fields = self.quill_fields
        return form

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Brend)
class BrendAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('banner_link',)
    search_fields = ('banner_link',)

@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'stock_quantity')
    # list_filter = ('color',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__first_name', 'user__last_name')
admin.site.register(Color)
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'address')
    search_fields = ('first_name', 'last_name', 'phone_number')