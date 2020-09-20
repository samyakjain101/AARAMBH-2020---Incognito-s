from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
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