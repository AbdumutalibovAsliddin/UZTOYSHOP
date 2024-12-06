from django.urls import path
from .views import register, verify, edit_profile,logout_view,login_view
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path('register/', register, name='register'),
    path('verify/<int:user_id>/', verify, name='verify'),
    path('profile/',edit_profile,name='profile'),
    path('logout/', logout_view, name='logout'),
    path('login/',login_view,name="login")
]
