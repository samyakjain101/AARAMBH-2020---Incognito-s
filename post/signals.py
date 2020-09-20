from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User
from .models import Post, Comment

def post_liked(sender, action, pk_set, instance, **kwargs):
    # Do something
    if action == 'post_add':
        #Send Notification to instance.author
        pass
            

m2m_changed.connect(post_liked, sender=Post.likes.through)