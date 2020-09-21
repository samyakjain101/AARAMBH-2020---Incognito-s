from django import template
from django.contrib.auth.models import User

register = template.Library()

def notificationcount(user):
    user = User.objects.get(id=user.id)
    count = user.profile.notificationcount
    return count

register.filter('notificationcount', notificationcount)