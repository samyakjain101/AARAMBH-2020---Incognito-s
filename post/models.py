from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='post')
    likes = models.ManyToManyField(User, related_name = 'post_likes', blank=True)
    comments = models.ManyToManyField(User, through='Comment', related_name = 'post_comments')

    def __str__(self):
        return str(self.author)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)

    

