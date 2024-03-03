from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from django.db import models
from django.template.loader import render_to_string
from .models import Post
from user_forms.models import User_Participate_Form
import threading

# email
from django.core.mail import EmailMessage

# date time
import datetime

# importing settings
from django_project.settings import EMAIL_HOST_USER

# os import
import os


# Threading Class
class EmailThread(threading.Thread) :
    def __init__(self,email_message):
        self.email_message = email_message
        super().__init__(args=email_message,kwargs=email_message)

    def run(self):
        self.email_message.send()


# Sending Tha Mail If It is Updated
@receiver(post_save,sender=Post)
def save_profile(sender, instance, created, **kwargs):
    event_dates = datetime.date(instance.event_date.year,instance.event_date.month,instance.event_date.day).strftime('%B %d, %Y')
    email_subject = f'Event Have Been Updated Recently Check Out !'
    for form in User_Participate_Form.objects.filter(event_post=instance) :
        email_messages = render_to_string('users/emails/update_participate.html',
                                        {
                                            'name' : form.user_person.first_name,
                                            'hoster' : instance.author.username,
                                            'event_type' : instance.event_type,
                                            'title' : instance.title,
                                            'content' : instance.content,
                                            'district' : instance.district,
                                            'event_dates' : event_dates,
                                        }
                                    )
        Email = EmailMessage(
                    email_subject,
                    email_messages,
                    EMAIL_HOST_USER,
                    to=[form.user_person.email]
            )
        Email.content_subtype = 'html'
        EmailThread(email_message=Email).start()


# Event Image Delete
@receiver(post_delete,sender=Post)
def auto_delete_file_on_delete(sender,instance,**kwargs) :
    if not instance.event_poster_image == 'defaults/defaults.png' :
        instance.event_poster_image.delete(False)


# Event Image Change Delete
@receiver(models.signals.pre_save, sender=Post)
def auto_delete_file_on_change(sender,instance,**kwargs) :

   try :
       old_file = sender.objects.get(pk=instance.pk).event_poster_image
   except sender.DoesNotExist :
       return False

   new_file = instance.event_poster_image

   if not old_file == new_file :
       if os.path.isfile(old_file.path) :
           if not old_file == 'defaults/defaults.png' :
                os.remove(old_file.path)



# print(form.user_person.email)
