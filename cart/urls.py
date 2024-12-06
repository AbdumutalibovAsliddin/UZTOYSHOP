from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('',views.cart_view,name="cart"),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-to-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/', views.update_cart_item_quantity, name='update_cart_item'),
    path('checkout/',views.checkout,name="checkout"),
    path('create_address/',views.create_address,name="create_address"),
    path('update_address/<str:address_code>',views.update_address,name="update_address"),
    path('get_address/',views.get_address,name="get_address"),
    path('creat_order/',views.creat_order,name="creat_order"),
    path('save_order_date/', views.save_order_date, name='save_order_date'),
    path('order/cancel/', views.cancel_order, name='cancel_order'),
]
