from django.urls import path
from .views import *

app_name = 'chat'

urlpatterns = [
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('message/<room_name>/', RoomView.as_view(), name='room'),
    path('ajax/chat/new_room/', create_room, name='create_room'),
]
