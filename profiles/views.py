from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DetailView
from django.views.generic.edit import UpdateView #for edit profile
from django.urls import reverse
from .forms import *
# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        if self.request.user.is_authenticated:
            profilePerc = self.request.user.profile.getPerc()
            context["profilePerc"] = profilePerc    
        return context

class UserRegistration(CreateView):
    model = User
    form_class = UserRegistrationForm

    template_name = "registration/user_form.html"

    def form_valid(self, form):
        if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            
            return render(self.request,'registration/register_success.html')
        else:
            return super().form_valid(form)

class ProfileView(TemplateView): #this is self view
    template_name = "profiles/profilepage.html"
    def get_context_data(self, **kwargs):
        profile = Profile.objects.get(user=User.objects.get(id=self.request.user.id))
        context = {
            'profile' : profile,
            'refer' : "self" #this is ensuring all self view components load up
            }
        return context

class EditProfile(UpdateView):
    
    def get_object(self):
        return get_object_or_404(Profile, user__username=self.request.user.username)

    model = Profile
    fields = [
        'profile_photo', 
        'phone', 
        'address', 
        'profession', 
        'facebook', 
        'instagram', 
        'linkedin'
        ] # Keep listing whatever fields 
    
    template_name = 'profiles/editprofile.html'

    def get_success_url(self):
        success_url = '/'
        return success_url

class ProfileDetailView(DetailView): #this is for global page
    object = Profile
    template_name = "profiles/profilepage.html"

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])
    
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        context["refer"] = "global" 
        context["profileUser"] = self.kwargs['username']
        return context
