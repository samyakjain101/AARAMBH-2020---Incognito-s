from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog/',views.BlogView.as_view(),name='blog_view_new'),
    path('blog/<pk>',views.BlogDetailView.as_view(),name='blog_detail_view'),
    path('create_blog/',views.CreateBlog.as_view(),name='create_blog'),
    path('manage_blog/',views.ManageBlog.as_view(),name='manage_blog'),
    path('manage_blog/edit/<pk>',views.EditBlog.as_view(),name='blog_edit'),
    path('manage_blog/delete/<pk>',views.BlogDelete.as_view(),name='blog_delete'),
    path('manage_blog/blog/<pk>',views.ManageBlogDetailView.as_view(),name='manage_blog_detail_view'),
]
