from django.shortcuts import render
from django.views.generic import TemplateView
from profiles.models import ConnectionRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification
# Create your views here.

class NotificationView(LoginRequiredMixin,TemplateView):
    template_name = "notification/notification.html"
    def get_context_data(self, **kwargs):
        notifications = Notification.objects.filter(to_user=self.request.user,seen=False)
        for notification in notifications:
            notification.seen=True
            notification.save()

        connection_requests = ConnectionRequest.objects.filter(to_user=self.request.user)
        context = {
            'notifications' : notifications,
            'connection_requests' : connection_requests
            }
        return context