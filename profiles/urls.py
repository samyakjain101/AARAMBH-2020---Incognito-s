from django.urls import path
from .views import *

app_name = 'profiles'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/',UserRegistration.as_view(),name="register"),
]
