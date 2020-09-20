import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
# Create your views here.

@login_required
def feed_view(request):
    connections = [x.user for x in User.objects.get(id=request.user.id).profile.connections.all()]
    feeds = Post.objects.filter(author__in = connections)
    if request.method == "POST":
        if request.is_ajax():
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.save()
                print("Valid Form")
            else:
                form = PostForm()
                print("Invalid Form")
        else:
            form = PostForm()
        
    else:
        form = PostForm()
    return render(request, "post/feed.html" , context = {'feeds': feeds, 'form':form})

class PostDetailView(LoginRequiredMixin ,DetailView):
    model = Post

@login_required
def toggle_like_post(request):
    jsonr = {}
    if request.is_ajax():
        user = request.user
        post_id = request.GET.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
            if user in post.likes.all():
                post.likes.remove(user)
                jsonr['likes_count'] = post.likes.count()
                jsonr['message'] = 'disliked'
            else:
                post.likes.add(user)
                jsonr['likes_count'] = post.likes.all().count()
                jsonr['message'] = 'liked'
        except ObjectDoesNotExist:
            jsonr['message'] = 'Something went wrong.'
            
    return HttpResponse(json.dumps(jsonr), content_type='application/json')