from django.contrib import admin
from .models import Profile, ConnectionRequest

# Register your models here.
admin.site.register(Profile)
admin.site.register(ConnectionRequest)