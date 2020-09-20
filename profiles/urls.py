from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
app_name = 'profiles'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/',UserRegistration.as_view(),name="register"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
