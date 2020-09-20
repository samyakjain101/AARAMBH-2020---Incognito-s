import json
import uuid
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Chat

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

class RoomView(LoginRequiredMixin, TemplateView):
    template_name = "chat/room.html"
    def get_context_data(self, **kwargs):

        # If room does not exist or id someone is trying to join a room of which he/she is not part of. Permission Denied
        try:
            room_name = uuid.UUID(self.kwargs['room_name']).hex
        except ValueError:
            raise PermissionDenied("Permission Denied")
        
        try:
            chat = Chat.objects.get(chat_id = room_name, room = self.request.user.id)
            for user in chat.room.all():
                if user == self.request.user:
                    pass
                else:
                    user2 = user
        except ObjectDoesNotExist:
            raise PermissionDenied("Permission Denied")
        
        contacts = Chat.objects.filter(room = self.request.user.id)

        context = {
            'room_name': self.kwargs['room_name'],
            'current_user': self.request.user.username,
            'user2': user2,
            'chat' : chat,
            'contacts' : contacts,
            }
        return context
