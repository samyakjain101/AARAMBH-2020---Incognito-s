from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from .models import Chat

# Create your views here.
class InboxView(LoginRequiredMixin, TemplateView):
    template_name = "chat/inbox.html"
    def get_context_data(self, **kwargs):
        users = User.objects.all()
        chats = Chat.objects.filter(room = self.request.user.id)
        context = {
            'users': users,
            'chats': chats,
            }
        return context