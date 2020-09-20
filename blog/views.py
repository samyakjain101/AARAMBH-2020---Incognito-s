from blog.models import Blog
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from  django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
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
    # define get_absolute_url instead later
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
        # Adding Permissions to edit and delete this blog for user

        current_user = User.objects.get(id = self.request.user.id)

        # assign_perm('edit_own_blog', current_user , blog)
        # assign_perm('delete_own_blog', current_user , blog)

        return super().form_valid(form)

class ManageBlog(LoginRequiredMixin,ListView):
    template_name = 'blog/blog_manage.html'
    model = Blog
    def get_queryset(self):
        queryset_original = super().get_queryset()
        return queryset_original.filter(user=self.request.user.id).order_by('-date')

class EditBlog(LoginRequiredMixin,UpdateView):
    permission_required = 'blog.edit_own_blog'
    model = Blog
    fields = ['title','text','image']

    def form_valid(self,form):

        if "upload" in self.request.POST:
            form.instance.draft = False
        else:
            form.instance.draft = True

        form.save()
        return super().form_valid(form)


class BlogDelete(LoginRequiredMixin,DeleteView):
    permission_required = 'blog.delete_own_blog'
    model = Blog
    success_url = reverse_lazy('blog:manage_blog')

class ManageBlogDetailView(DetailView):
    template_name = "blog/blog_manage_detail_view.html"
    model = Blog
    def get_queryset(self):
        queryset_original = super().get_queryset()
        return queryset_original.filter(user=self.request.user.id).order_by('-date')
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['x'] = self.object.text.split("\n")
        data['recent_blogs'] = Blog.objects.filter(display=True,draft=False).exclude(id=self.object.id).order_by('-date')[:3]
        return data