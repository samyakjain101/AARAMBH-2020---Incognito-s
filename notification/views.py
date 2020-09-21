from django.shortcuts import render
from django.views.generic import TemplateView
from profiles.models import ConnectionRequest
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class Notification(LoginRequiredMixin,TemplateView):
    template_name = "notification/notification.html"
    def get_context_data(self, **kwargs):
        connection_requests = ConnectionRequest.objects.filter(to_user=self.request.user)
        context = {
            'connection_requests' : connection_requests
            }
        return context