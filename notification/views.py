from django.shortcuts import render
from django.views.generic import TemplateView
from profiles.models import ConnectionRequest
# Create your views here.

class Notification(TemplateView):
    template_name = "notification/notification.html"
    def get_context_data(self, **kwargs):
        connection_requests = ConnectionRequest.objects.filter(to_user=self.request.user)
        context = {
            'connection_requests' : connection_requests
            }
        return context