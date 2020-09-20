from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('inbox/', views.InboxView.as_view(), name='inbox'),
]
