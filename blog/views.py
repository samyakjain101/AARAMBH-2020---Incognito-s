from blog.models import Blog
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

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

class CreateBlog(LoginRequiredMixin,CreateView):
    model = Blog
    fields = ('title','text','image')
    success_url = reverse_lazy('blog:manage_blog')
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        from django import forms
        form = super(CreateBlog, self).get_form(form_class)
        form.fields['title'].widget = forms.TextInput(attrs={'placeholder': 'Title'})
        form.fields['text'].widget = forms.Textarea(attrs={'placeholder': 'Blog Text Here'})
        return form

    def form_valid(self,form):
        blog = form.save(commit=False)
        blog.user = self.request.user
        blog.display = False

        if "upload" in self.request.POST:
            blog.draft = False
        else:
            blog.draft = True

        form.save()
        current_user = User.objects.get(id = self.request.user.id)
        return super().form_valid(form)
