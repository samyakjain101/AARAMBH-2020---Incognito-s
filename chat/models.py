import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    chat_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ManyToManyField(User)

    def __str__(self):
        return str(self.chat_id)