from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import threading

# forms
from .forms import UserRegisterForm, UserUpdateForm,ProfileUpdateForm

# model
from django.contrib.auth.models import User

# email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage

# Object Of Password Token Generator
generate_token = PasswordResetTokenGenerator()

# email host
from django_project.settings import EMAIL_HOST_USER


# Threading Class
class EmailThread(threading.Thread) :
    def __init__(self,email_message):
        self.email_message = email_message
        super().__init__(args=email_message,kwargs=email_message)

    def run(self):
        self.email_message.send()

# Create your views here.
def register(request):
    if request.method == 'POST' :
        form = UserRegisterForm(request.POST)

        if User.objects.filter(email=form['email'].value()).exists() :
            form.add_error('email','Email Already Exists')

        if form.is_valid() :
            user = form.save(commit=False)
            messages.info(request, f'Click on Confirmation Mail Sent to You')
            user.is_active = False
            user.save()

            current_site = get_current_site(request)

            email_subject = 'Activate Your Account, Eventorr Team'
            email_messages = render_to_string('users/emails/activate.html',
                                        {
                                            'user' : user,
                                            'domain' : current_site.domain,
                                            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                                            'token' : generate_token.make_token(user=user),
                                        }
                                       )

            email_message = EmailMessage(
                email_subject,
                email_messages,
                EMAIL_HOST_USER,
                [form['email'].value()],
            )
            email_message.content_subtype = 'html'
            EmailThread(email_message=email_message).start()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})



# Account Activation By Email
def ActivateAccountView(request,uidb64,token) :
    try :
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError) :
        user = None

    if user is not None and generate_token.check_token(user,token) :
        user.is_active = True
        user.save()

        messages.info(request, f'Account Activated Successfully, Please Login !')
        return redirect('login')
    else:
        return render(request,'users/emails/activate_failed.html',status=401)



# profile function based view
@login_required
def profile(request) :
    if request.method == 'POST' :
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid() :
            u_form.save()
            p_form.save()
            messages.info(request, f'Your Account Is Has been Updated !')
            return redirect('profile')

    else :
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }

    return render(request, 'users/profile.html', context)



# logout function based view
def logout(request):
    auth.logout(request)
    messages.info(request, f'You Have been Logged Out !')
    return redirect('login')

