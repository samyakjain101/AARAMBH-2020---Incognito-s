from django.urls import path
from .views import *

app_name = 'notification'

urlpatterns = [
    path("notification/", Notification.as_view(), name="notification"),
]
