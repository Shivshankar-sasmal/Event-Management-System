from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# models
from event.models import Post

# Create your models here.
class User_Participate_Form(models.Model) :
    user_person = models.ForeignKey(User, on_delete=models.CASCADE)
    event_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    form_date = models.DateTimeField(default=timezone.now)
    phone = models.IntegerField(help_text='Phone Number Without Country Code')
    college = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.user_person} - {self.event_post}'

    def get_absolute_url(self):
        return ('/')

