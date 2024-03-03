# Generated by Django 3.0.5 on 2020-07-04 03:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=75)),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('event_date', models.DateField(help_text='Date Is Present in MM-DD-YY format', null=True)),
                ('event_poster_image', models.ImageField(default='defaults/defaults.jpg', help_text='Upload a 800 x 400 Image', upload_to='poster')),
                ('max_seats', models.PositiveIntegerField()),
                ('event_type', models.CharField(help_text='eg. Programming, Working, Dance, etc.', max_length=20)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='event.District')),
                ('fake_post_report', models.ManyToManyField(blank=True, related_name='fake_post', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
