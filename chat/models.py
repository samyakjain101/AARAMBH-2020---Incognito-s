import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ManyToManyField(User)

    @property
    def last_message(self):
        return self.message_set.latest('timestamp').content
        
    def __str__(self):
        return str(self.chat_id)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content =  models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['timestamp']

    def __str__(self):
        return self.author.username
    
    def last_10_messages():
        return Message.objects.order_by('timestamp').all()[:10]