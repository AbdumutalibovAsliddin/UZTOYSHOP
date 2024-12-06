from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('',views.dashboard_home,name="home"),
    path('login/',views.login_view,name="login"),
    path('register/',views.register,name="register"),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('product_list/',views.product_list,name="product_list"),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('create/', views.product_create, name='create_product'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('barcode_view/',views.barcode_view,name="barcode_view"),
    path('barcode/<str:barcode>/',views.barcode_detail_view,name="barcode_detail"),
    path('contacts/',views.contact_view,name="contact_view"),
    path('message/<int:message_id>/', views.message_detail, name='message_detail'),
    path('orders/',views.orders_view,name="orders_view"),
    path('order/<int:pk>/',views.order_detail,name="order_detail"),
    path('edit_order_status/',views.edit_order_status,name="order_status"),
    path('sellers/',views.seller_view,name="seller_view"),
    path('delete-user/<int:pk>/', views.UserProfileDeleteView.as_view(), name='delete_user'),
    path('total_order/',views.total_order,name="total_order"),
    path('logout/', views.logout_view, name='logout'),  # Logout URL
]