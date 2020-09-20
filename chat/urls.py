from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('inbox/', views.InboxView.as_view(), name='inbox'),
    path('message/<room_name>/', views.RoomView.as_view(), name='room'),
]
