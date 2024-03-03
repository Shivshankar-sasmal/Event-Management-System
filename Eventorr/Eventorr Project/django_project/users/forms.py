from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#models
from event.models import District
from .models import Profile
from user_forms.models import User_Participate_Form


# Forms
class UserRegisterForm(UserCreationForm) :
     first_name = forms.CharField(label='Full Name')
     last_name = forms.ChoiceField(label='District',choices=[[i,i] for i in District.objects.all() ])
     email = forms.EmailField()

     class Meta :
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']


class UserUpdateForm(forms.ModelForm) :
    first_name = forms.CharField(label='Full Name')
    last_name = forms.ChoiceField(label='District', choices=[[i,i] for i in District.objects.all() ])

    class Meta :
        model = User
        fields = ['first_name','last_name','username']


class ProfileUpdateForm(forms.ModelForm) :
    class Meta :
        model = Profile
        fields = ['image','about_you']

class User_P_Form(forms.ModelForm) :
    phone = forms.IntegerField(min_value=5555555555,max_value=9999999999,help_text='Enter Mobile Number Without Country Code')
    college = forms.CharField(max_length=150)

    class Meta :
        model = User_Participate_Form
        fields = ['phone', 'college']
