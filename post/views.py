import json
from django.shortcuts import render
from django.core.mail import BadHeaderError, send_mail #for sending mail
from django.conf import settings # for getting from mail (sending mail)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.detail import DetailView

from django.http import HttpResponse, HttpResponseRedirect
from .models import Post, Comment

from .forms import PostForm
# Create your views here.

def send_notification(to_user, message):
    group_name = 'chat_%s' % to_user.username
    channel_layer = channels.layers.get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'chat_message',
            'message': message
        }
    )

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

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

import channels.layers
from asgiref.sync import async_to_sync

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

                #Send notification to Person whose post is liked
                message = '{} {} liked your post'.format(user.first_name,user.last_name)
                subject = "You have 1 notification"
                from_email = settings.EMAIL_HOST_USER
                to_mail = [post.author.email]
                send_notification(post.author, message)
                #Send email to Person whose post is liked
                message = '{} {} liked your post \n {}'.format(user.first_name,user.last_name,post.content)
                send_email(subject,message,from_email,to_mail)

        except ObjectDoesNotExist:
            jsonr['message'] = 'Something went wrong.'
            
    return HttpResponse(json.dumps(jsonr), content_type='application/json')


@login_required
def post_comment(request):
    jsonr = {}
    if request.is_ajax():
        post_id = request.POST.get('post_id')
        comment = request.POST.get('comment')
        try:
            post = Post.objects.get(id=post_id)
            user = User.objects.get(id=request.user.id)
            Comment.objects.create(
                user = user,
                post = post,
                comment = comment
            )
            jsonr['message'] = 'Success'

            #Send notification to Person whose post is commented
            message = '{} {} commented on your post'.format(user.first_name,user.last_name)
            subject = "You have 1 notification"
            from_email = settings.EMAIL_HOST_USER
            to_mail = [post.author.email]
            send_notification(post.author, message)
            #Send email to Person whose post is commented
            message = '{} {} commented on your post \n {}'.format(user.first_name,user.last_name,post.content)
            send_email(subject,message,from_email,to_mail)

        except ObjectDoesNotExist:
            jsonr['message'] = 'Something went wrong.'
            
    return HttpResponse(json.dumps(jsonr), content_type='application/json')


def send_email(subject,message,from_email,to_mail):
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, to_mail, fail_silently=True)
        except BadHeaderError:
            send_mail("Invalid header found in sent below email", "Subject : " + subject + "\n" + "Message : " + message, from_email, from_email, fail_silently=True)
            #return HttpResponse('Invalid header found.')
        #return HttpResponseRedirect('/contact/thanks/')
    else:
        send_mail("all field not filled error in sent below email", "Subject : " + subject + "\n" + "Message : " + message, from_email, from_email, fail_silently=True)

