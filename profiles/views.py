import re
import string
import json
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse
from blog.models import Blog
from post.models import Post
from .forms import *
from .models import *
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


# class ProfileView(TemplateView): #this is self view
#     template_name = "profiles/profilepage.html"
#     def get_context_data(self, **kwargs):
#         profile = Profile.objects.get(user=User.objects.get(id=self.request.user.id))
#         context = {
#             'profile' : profile,
#             'refer' : "self" #this is ensuring all self view components load up
#             }
#         return context

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
        success_url = '/profile'
        return success_url


class ProfileDetailView(DetailView): #this is for global page
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