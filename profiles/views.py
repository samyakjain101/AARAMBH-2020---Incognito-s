import re
import string
import json
from django.utils import timezone
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse
from blog.models import Blog
from post.models import Post
from .forms import *
from .models import *
from django.core.mail import BadHeaderError, send_mail #for sending mail
from post.views import send_notification, send_email
# Create your views here.

def anonymous_required(function=None, redirect_url=None):

   if not redirect_url:
       redirect_url = settings.LOGIN_REDIRECT_URL

   actual_decorator = user_passes_test(
       lambda u: u.is_anonymous,
       login_url=redirect_url
   )

   if function:
       return actual_decorator(function)
   return actual_decorator


class IndexView(LoginRequiredMixin,TemplateView):
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

class EditProfile(LoginRequiredMixin,UpdateView):

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
        success_url = '/profile/' + self.request.user.username
        return success_url
    
    def get_object(self):
        return get_object_or_404(Profile, user__username=self.request.user.username)
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        from django import forms
        form = super(EditProfile, self).get_form(form_class)
        form.fields['phone'].widget = forms.TextInput(attrs={'placeholder': ' Phone','class': 'form-control'})
        form.fields['profession'].widget = forms.TextInput(attrs={'placeholder': ' Profession','class': 'form-control'})
        form.fields['facebook'].widget = forms.TextInput(attrs={'placeholder': ' Facebook','class': 'form-control'})
        form.fields['instagram'].widget = forms.TextInput(attrs={'placeholder': ' Instagram','class': 'form-control'})
        form.fields['linkedin'].widget = forms.TextInput(attrs={'placeholder': ' LinkedIn','class': 'form-control'})
        form.fields['address'].widget = forms.Textarea(attrs={'placeholder': ' Somewhere','class': 'form-control'})
        return form



class ProfileDetailView(DetailView):
    object = Profile
    template_name = "profiles/profilepage.html"

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])
    
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)        

        if self.request.user.username == self.kwargs['username']:
            context["refer"] = "self"
        else:
            context["refer"] = "global"

        context["posts"] = Post.objects.filter(author = User.objects.get(username=self.kwargs['username']))
        context["globalUsername"] = self.kwargs['username']
        context["globalUser"] = User.objects.get(username=self.kwargs['username'])
        context["globalProfile"] = Profile.objects.get(user=User.objects.get(username=self.kwargs['username']))
        return context

def search(request):
    search_text = request.GET.get('search')
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    porter = PorterStemmer()

    u = Q()
    b = Q()
    p = Q()

    for token in word_tokenize(search_text):
        new_token = regex.sub(u'', token)
        if not new_token == u'' and not token in stopwords.words('english'):
            new_token_stem = porter.stem(new_token)
            u |= Q(username__icontains = new_token)
            b |= Q(title__icontains = new_token_stem)
            p |= Q(content__icontains = new_token_stem)

    users = User.objects.filter(u)
    blogs = Blog.objects.filter(b)
    posts = Post.objects.filter(p)

    return render(request, "profiles/search.html" , context = {'users': users, 'blogs':blogs, 'posts':posts})

@login_required
def accept_connection_request(request):
    jsonr = {}
    if request.is_ajax():
        current_user = User.objects.get(id=request.user.id)
        current_user_profile = Profile.objects.get(user=User.objects.get(id=request.user.id))
        sender_id = request.GET.get('sender') #User who sent the request
        try:
            sender = User.objects.get(id=sender_id)
            sender_profile = Profile.objects.get(user=User.objects.get(id=sender_id))
            current_user_profile.connections.add(sender_profile)
            # if created: 
            #     jsonr['message'] = "Friend request sent"
            # else:
            #     jsonr['message'] = "Friend request already sent"
            delete_request = ConnectionRequest.objects.get(from_user=sender,to_user=current_user)
            delete_request.delete()
            jsonr['message'] = "Friend request accepted"

            #Send notification to Person whose request is accepted
            message = '{} {} accepted your connection request'.format(current_user.first_name,current_user.last_name)
            subject = "You have 1 notification"
            from_email = settings.EMAIL_HOST_USER
            to_mail = [sender.email]
            send_notification(current_user, sender, message)
            #Send email to Person whose request is accepted
            message = '{} {} accepted your connection request.'.format(current_user.first_name,current_user.last_name)
            send_email(subject,message,from_email,to_mail)

        except ObjectDoesNotExist:
            jsonr['error'] = "User does not exist"
        
    return HttpResponse(json.dumps(jsonr), content_type='application/json')

@login_required
def reject_connection_request(request):
    jsonr = {}
    if request.is_ajax():
        current_user = User.objects.get(id=request.user.id)
        current_user_profile = Profile.objects.get(user=User.objects.get(id=request.user.id))
        sender_id = request.GET.get('sender') #User who sent the request
        try:
            sender = User.objects.get(id=sender_id)
            sender_profile = Profile.objects.get(user=User.objects.get(id=sender_id))
            delete_request = ConnectionRequest.objects.get(from_user=sender,to_user=current_user)
            delete_request.delete()
            jsonr['message'] = "Friend request rejected"

        except ObjectDoesNotExist:
            jsonr['error'] = "User does not exist"
        
    return HttpResponse(json.dumps(jsonr), content_type='application/json')

# Need some changes. If two people are already friend then can't send request. Handle this case
@login_required
def send_connection_request(request):
    jsonr = {}
    if request.is_ajax():
        from_user = User.objects.get(id=request.user.id)
        to_user_id = request.GET.get('user_id')
        try:
            to_user = User.objects.get(id=to_user_id)
            if not Profile.objects.filter(user=from_user,connections=to_user.profile).exists():
                obj, created = ConnectionRequest.objects.get_or_create(to_user = to_user, from_user = from_user)
                if created:
                    jsonr['message'] = "Connection request sent"

                    #Send notification to Person to whom request is sent
                    message = '{} {} requested to connect to you'.format(from_user.first_name,from_user.last_name)
                    subject = "You have 1 notification"
                    from_email = settings.EMAIL_HOST_USER
                    to_mail = [to_user.email]
                    send_notification(from_user, to_user, message)
                    #Send email to Person to whom request is sent
                    message = '{} {} requested to connect to you.'.format(from_user.first_name,from_user.last_name)
                    send_email(subject,message,from_email,to_mail)

                else:
                    obj.created = timezone.now()
                    jsonr['message'] = "Connection request already sent"
            else:
                jsonr['message'] = "Connection already exists."
                
        except ObjectDoesNotExist:
            jsonr['error'] = "User does not exist"
        
    return HttpResponse(json.dumps(jsonr), content_type='application/json')