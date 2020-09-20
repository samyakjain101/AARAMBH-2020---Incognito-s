from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name = 'blog_user')
    title = models.CharField(max_length=50)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    display = models.BooleanField()
    draft = models.BooleanField()
    image = models.ImageField(upload_to='blogs/',blank=True)
    
    class Meta():
        unique_together=['user','title']

    def get_absolute_url(self):
        from django.urls import reverse_lazy
        return reverse_lazy('blog:manage_blog')

    def get_edit_url(self):
        from django.urls import reverse
        return reverse('blog:blog_edit', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
