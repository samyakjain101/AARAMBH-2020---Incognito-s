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
        contacts = Chat.objects.filter(room = self.request.user.id)
        context = {
            'users': users,
            'contacts': contacts,
            }
        return context

class RoomView(LoginRequiredMixin, TemplateView):
    template_name = "chat/room.html"
    def get_context_data(self, **kwargs):

        # If room does not exist or if someone is trying to join a room of which he/she is not part of. Permission Denied
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
            'users' : User.objects.exclude(id=self.request.user.id),
            'room_name': self.kwargs['room_name'],
            'current_user': self.request.user.username,
            'user2': user2,
            'chat' : chat,
            'contacts' : contacts,
            }
        return context

# Create New Chat room if it does not exist already.
@login_required
def create_room(request):
    jsonr = {}
    if request.is_ajax():
        current_user = User.objects.get(id = request.user.id)
        try:
            user_id = User.objects.get(id = request.GET.get('user_id'))
            if not current_user == user_id:
                chat_obj = Chat.objects.filter(room = current_user).filter(room = user_id)
                if not chat_obj.exists():
                    obj = Chat.objects.create(chat_id = uuid.uuid4())
                    obj.room.add(current_user, user_id)
                    jsonr['redirect'] = str(obj.chat_id)
                else:
                    if chat_obj.count() == 1:
                        jsonr['redirect'] = str(chat_obj[0].chat_id)
                    print('Room already exists')
            else:
                print("Can't chat to yourselves, right now")
        except ObjectDoesNotExist:
            raise PermissionDenied
    return HttpResponse(json.dumps(jsonr), content_type='application/json')
