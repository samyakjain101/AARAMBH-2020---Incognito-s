from django.urls import path
from .views import *

app_name = 'notification'

urlpatterns = [
    path("test", test, name="test")
]
