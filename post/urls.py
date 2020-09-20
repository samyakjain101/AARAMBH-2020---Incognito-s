from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('feeds/', views.feed_view, name='feed'),
]
