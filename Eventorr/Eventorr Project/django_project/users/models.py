from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='defaults/default.png', upload_to='profile_pics')
    about_you = models.TextField(max_length=400, null=True, default='I want to Describe Myself as Being very Resourceful and Ambitious at the same time.', help_text='Tell Us Something About Yourself')

    def __str__(self):
        return f'Profile - {self.user.username}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None,*args,**kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.image.path)
        img.thumbnail((250,250))
        img.save(self.image.path)
