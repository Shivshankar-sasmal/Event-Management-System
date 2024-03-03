from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import threading

# email
from django.core.mail import EmailMessage

# date time
import datetime

# models
from user_forms.models import User_Participate_Form
from event.models import Post
from django_project.settings import EMAIL_HOST_USER

# forms
from users.forms import User_P_Form


# Threading Email Class
class EmailThread(threading.Thread) :
    def __init__(self,email_message):
        self.email_message = email_message
        super().__init__(args=email_message,kwargs=email_message)

    def run(self):
        self.email_message.send()

class User_Participation_Form(LoginRequiredMixin, CreateView) :
    def get(self, request, *args, **kwargs):
        return render(request, 'user_forms/user_participate_form_form.html', {'form': User_P_Form})

    def post(self, request, *args, **kwargs):
        form = User_P_Form(request.POST)

        if form.is_valid() :
            form.instance.user_person = self.request.user
            posts = get_object_or_404(Post,pk=self.kwargs.get('pk'))
            form.instance.event_post = posts

            print(f'Number :')

            if User_Participate_Form.objects.filter(event_post=posts,user_person=self.request.user).exists() :
                messages.success(request,'You Have Already Participated')
                
            elif posts.max_seats != User_Participate_Form.objects.filter(event_post=posts).count() :
                form.save()
                messages.info(request,'Participation Form is Submitted Successfully !')
                event_dates = datetime.date(posts.event_date.year,posts.event_date.month,posts.event_date.day).strftime('%B %d, %Y')
                name = self.request.user.first_name

                # Email Message
                email_subject = f'Participation Form is Submitted Successfully !'
                email_messages = render_to_string('users/emails/participate.html',
                                                {
                                                    'name' : name,
                                                    'hoster' : posts.author.username,
                                                    'event_type' : posts.event_type,
                                                    'title' : posts.title,
                                                    'content' : posts.content,
                                                    'district' : posts.district,
                                                    'event_dates' : event_dates,
                                                }
                                               )
                Email = EmailMessage(
                    email_subject,
                    email_messages,
                    EMAIL_HOST_USER,
                    to=[self.request.user.email]
                )
                Email.content_subtype = 'html'
                EmailThread(email_message=Email).start()

            else :
                messages.warning(request,'Sorry, Participation List is Full for this Event !')

            return redirect('/')



# Delete Form
@login_required
def DeleteForm(request, post_pk, form_pk) :
    user_name = Post.objects.get(pk=post_pk).author.username

    if user_name == request.user.username :
        User_Participate_Form.objects.get(id=form_pk).delete()
        messages.info(request, 'Form Deleted Successfully')
        return redirect('./')

    messages.warning(request, 'You Are not Allowed To Delete Others Form')
    return redirect('/')
