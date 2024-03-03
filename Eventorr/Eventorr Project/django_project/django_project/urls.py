"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views



# app urls views
from event.views import (
     about,
     PostListView,
     PostDetailView,
     PostCreateView,
     PostUpdateView,
     PostDeleteView,
     UserPostListView,
     FakePostReportRedirect,
)
from users import views as user_views
from user_forms.views import User_Participation_Form, DeleteForm


urlpatterns = [
    # Basic Url
    path('admin/', admin.site.urls),
    path('', PostListView.as_view(), name='event-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('about/', about, name='event-about'),
    path('register/', user_views.register, name='register'),
    path('profile/',user_views.profile, name='profile'),

    # Post View Url
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),

    # Fake_Post_Report Button
    path('post/<int:pk>/fake_post', FakePostReportRedirect.as_view(), name='fake_post_report'),

    # Form Create View
    path('post/<int:pk>/form', User_Participation_Form.as_view(), name='form_creation'),

    #Form Delete Function
    path('post/<int:post_pk>/<int:form_pk>',DeleteForm, name='form-delete'),

    # Login and Logout Url
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', user_views.logout, name='logout'),

    # Email Account Activation
    path('activate/<uidb64>/<token>',user_views.ActivateAccountView, name='activate'),

    # Password Reset Tokens
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset.html'), name='password_reset_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

