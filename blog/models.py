from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime 

class Blog(models.Model):  
    pub_date = models.DateTimeField(auto_now=True)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.body    

class Profile(models.Model):
    date = datetime.datetime.now() - datetime.timedelta(days=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    last_date = models.DateTimeField(default=date, blank=True)  

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()    