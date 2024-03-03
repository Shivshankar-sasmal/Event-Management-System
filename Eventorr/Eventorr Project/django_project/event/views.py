from django.shortcuts import render, get_object_or_404,reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    RedirectView,
)

# importing datetime
from django.utils import timezone

# models
from .models import Post
from user_forms.models import User_Participate_Form

#Query
from django.db.models import Q

#Threading Import
import threading

#email
from django.core.mail import EmailMessage

#email host
from django_project.settings import EMAIL_HOST_USER

# Threading Class
class EmailThread(threading.Thread) :
    def __init__(self,email_message):
        self.email_message = email_message
        super().__init__(args=email_message,kwargs=email_message)

    def run(self):
        self.email_message.send()


# Fucntion Based View
def about(request) :
    return render(request,'event/about.html')


#Class Views
class PostListView(ListView) :
    model = Post
    template_name = 'event/home.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            search = search.strip()
            return Post.objects.filter(
                ( Q(event_type__icontains=search) |
                Q(content__icontains=search) |
                Q(title__icontains=search) |
                Q(district__district__icontains=search) |
                Q(author__first_name__icontains=search) ) &
                ( Q(event_date__gte=timezone.now()) )
                ).distinct().order_by('event_date')
        else :
            return Post.objects.filter(event_date__gte=timezone.now()).order_by('event_date')


class UserPostListView(LoginRequiredMixin,ListView) :
    model = Post
    template_name = 'event/user_posts.html'
    context_object_name = 'posts'
    ordering = ['event_date']
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(Q(author__exact=user) & Q(event_date__gte=timezone.now())).order_by('event_date')

class PostDetailView(LoginRequiredMixin, DetailView) :
    queryset = Post.objects.all()
    template_name = 'event/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView,self).get_context_data(**kwargs)
        post = get_object_or_404(Post,pk=self.kwargs.get('pk'))
        context['forms'] = User_Participate_Form.objects.filter(event_post = post.id).order_by('form_date')
        return context


class PostCreateView(LoginRequiredMixin, CreateView) :
    model = Post
    fields = ['title','content','event_poster_image','event_date','district','event_type', 'max_seats','college_url']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView) :
    model = Post
    fields = ['title','content','event_poster_image','event_date','district','event_type', 'max_seats','college_url']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author :
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView) :
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author :
            return True
        return False


class FakePostReportRedirect(LoginRequiredMixin,RedirectView) :

    def get_redirect_url(self, *args, **kwargs):
        object = get_object_or_404(Post,pk=self.kwargs.get('pk'))
        user = self.request.user

        if user in object.fake_post_report.all() :
            object.fake_post_report.remove(user)
        else :
            object.fake_post_report.add(user)
            if object.fake_post_report.count() == 100 :
                # Email Message
                email_subject = f'Your Post Is Been Deleted, by Administrator'
                email_messages = render_to_string('users/emails/delete_post.html',
                                                    {
                                                        'name' : object.author.first_name,
                                                        'hoster' : object.author.username,
                                                        'event_type' : object.event_type,
                                                        'title' : object.title,
                                                        'content' : object.content,
                                                        'district' : object.district,
                                                        'event_dates' : object.event_date,
                                                    }
                                                )
                Email = EmailMessage(
                        email_subject,
                        email_messages,
                        EMAIL_HOST_USER,
                        to=[object.author.email]
                    )
                Email.content_subtype = 'html'
                EmailThread(email_message=Email).start()
                object.delete()
                return reverse('event-home')

        return object.get_absolute_url()


