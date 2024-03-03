from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models

# models
from .models import Profile


# os import
import os


# Creating The Profile For Users
@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created :
        Profile.objects.create(user=instance)

#Saving The Profile For Users
@receiver(post_save,sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()


# Event Image Delete
@receiver(post_delete,sender=Profile)
def auto_delete_file_on_delete(sender,instance,**kwargs) :
    if not instance.image == 'defaults/default.png' :
        instance.image.delete(False)


# Event Image Change Delete
@receiver(models.signals.pre_save, sender=Profile)
def auto_delete_file_on_change(sender,instance,**kwargs) :

   try :
       old_file = sender.objects.get(pk=instance.pk).image
   except sender.DoesNotExist :
       return False

   new_file = instance.image

   if not old_file == new_file :
       if os.path.isfile(old_file.path) :
           if not old_file == 'defaults/default.png' :
                os.remove(old_file.path)
