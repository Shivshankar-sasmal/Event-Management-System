from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


# datetime

# Create your models here.
class District(models.Model) :
    district = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.district}'


class Post(models.Model) :
    title = models.CharField(max_length=75)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    event_date = models.DateField(null=True, help_text='Date Is Present in MM-DD-YY format')
    event_poster_image = models.ImageField(default='defaults/defaults.png', upload_to='poster', help_text='Upload a 800 x 400 Image')
    district = models.ForeignKey(District, on_delete=models.PROTECT)
    max_seats = models.PositiveIntegerField()
    fake_post_report = models.ManyToManyField(User,blank=True,related_name='fake_post')
    event_type = models.CharField(max_length=20, help_text='eg. Programming, Working, Dance, etc.')
    college_url = models.URLField(null=True, blank=True, help_text='eg. Pastes Event URL If Want')

    def __str__(self):
        return f'{self.title} {self.author}'

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_home_url(self):
        return reverse('event-home')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None,*args,**kwargs):
        super().save(*args,**kwargs)

        img = Image.open(self.event_poster_image.path)
        img.thumbnail((800,400))
        img.save(self.event_poster_image.path,optimize=True)

