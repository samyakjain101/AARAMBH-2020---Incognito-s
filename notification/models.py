from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Notification(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="to_user")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="from_user")

    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)

