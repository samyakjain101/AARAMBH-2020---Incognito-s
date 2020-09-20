from blog.models import Blog
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

# Create your views here.
class BlogView(TemplateView):
    template_name = "blog/blog.html"
    def get_context_data(self, **kwargs):
        blogs = Blog.objects.filter(display=True,draft=False).order_by('-date')
        context = {
            'blogs':blogs,
            }
        return context

class BlogDetailView(DetailView):
    queryset = Blog.objects.filter(display=True,draft=False).order_by('-date')
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['x'] = self.object.text.split("\n")
        data['recent_blogs'] = Blog.objects.filter(display=True,draft=False).exclude(id=self.object.id).order_by('-date')[:3]
        return data