from django.db import models
from main.models import Product, ProductColor
from account.models import UserProfile
# Create your models here.
class SoldProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to Product
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    sold_quantity = models.IntegerField()  # Quantity sold
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total sale price
    sale_date = models.DateTimeField(auto_now_add=True)  # Date of sale
    seller = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - Rangi: {self.product_color.color.name} - Miqdori: {self.sold_quantity}"