from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('blog/',BlogView.as_view(),name='blog_view_new'),
    path('blog/<pk>',BlogDetailView.as_view(),name='blog_detail_view'),
    path('create_blog/',CreateBlog.as_view(),name='create_blog'),
    path('manage_blog/',ManageBlog.as_view(),name='manage_blog'),
    path('manage_blog/edit/<pk>',EditBlog.as_view(),name='blog_edit'),
    path('manage_blog/delete/<pk>',BlogDelete.as_view(),name='blog_delete'),
    path('manage_blog/blog/<pk>',ManageBlogDetailView.as_view(),name='manage_blog_detail_view'),
    path('ajax/blog_comment/',blog_comment,name='blog_comment'),
]
