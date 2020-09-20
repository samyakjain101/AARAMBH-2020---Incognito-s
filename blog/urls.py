from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog/',views.BlogView.as_view(),name='blog_view_new'),
    path('blog/<pk>',views.BlogDetailView.as_view(),name='blog_detail_view'),
]
