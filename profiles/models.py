from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    facebook = models.URLField(max_length=100, blank=True, null=True)
    instagram = models.URLField(max_length=100, blank=True, null=True)
    linkedin = models.URLField(max_length=100, blank=True, null=True)
    connections = models.ManyToManyField("self", blank=True)
    profile_photo = models.ImageField(blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.user.username

    def getPerc(self):
        total=7 # currently 8 fields
        now=0
        if(self.profession): now+=1
        if(self.phone): now+=1
        if(self.address): now+=1
        if(self.facebook): now+=1
        if(self.instagram): now+=1
        if(self.linkedin): now+=1
        if(self.profile_photo): now+=1
        perc= (now/total)*100
        return int(perc)

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)