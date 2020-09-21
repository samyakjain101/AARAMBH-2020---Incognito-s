from django.urls import path
from .views import *

app_name = 'post'

urlpatterns = [
    path('', feed_view, name='feed'),
    path('feeds/<pk>/', PostDetailView.as_view(), name='feed_detail'),
    path('ajax/toggle_like_post/', toggle_like_post, name='toggle_like_post'),
    path('ajax/post_comment/', post_comment, name='post_comment'),
]
