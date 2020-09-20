from django.contrib import admin
from .models import Category, Notification, UserNotification
# Register your models here.

admin.site.register(Category)
admin.site.register(Notification)
admin.site.register(UserNotification)