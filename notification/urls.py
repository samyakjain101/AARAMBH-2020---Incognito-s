from django.urls import path
from .views import *

app_name = 'notification'

urlpatterns = [
    path("notification/", NotificationView.as_view(), name="notification"),
]
