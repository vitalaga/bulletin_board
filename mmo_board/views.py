from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView
)

from .models import Post, User, Category, Response
from .forms import PostFrom, UserForm, ResponseForm, ResponseAcceptForm
from .utils import ProfileOwnershipVerificationMixin
from bulletin_board.settings import DEFAULT_FROM_EMAIL, SITE_URL


class PostList(ListView):
    model = Post
    ordering = '-date_created'
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.queryset = Post.objects.all().select_related('author').defer(
            'author__password',
            'author__last_login',
            'author__is_superuser',
            'author__email',
            'author__is_staff',
            'author__is_active',
            'author__date_joined',
        ).prefetch_related('category')
        return super().get_queryset()


class CategoryList(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.queryset = Post.objects.filter(category__id=self.kwargs['category_id']).select_related('author').defer(
            'author__password',
            'author__last_login',
            'author__is_superuser',
            'author__email',
            'author__is_staff',
            'author__is_active',
            'author__date_joined',
        ).prefetch_related('category')
        return super().get_queryset()


class PostDetail(LoginRequiredMixin, CreateView):
    template_name = 'forms/post_response.html'
    form_class = ResponseForm

    def get_success_url(self) -> str:
        return reverse_lazy('post', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        responses = Response.objects.filter(approved=True).select_related('author').defer(
            'author__password',
            'author__last_login',
            'author__is_superuser',
            'author__email',
            'author__is_staff',
            'author__is_active',
            'author__date_joined',
        )
        context['post'] = Post.objects \
            .filter(pk=self.kwargs['pk']) \
            .select_related('author').defer(
            'author__password',
            'author__last_login',
            'author__is_superuser',
            'author__email',
            'author__is_staff',
            'author__is_active',
            'author__date_joined',
        ).prefetch_related(Prefetch('response_set', queryset=responses)) \
            .prefetch_related('category')[0]
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = User.objects.get(id=self.request.user.id)
        self.object.post = Post.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        link = reverse_lazy('post', kwargs={'pk': self.kwargs['pk']})
        subject = 'Under your post a new response!'
        message = f'{self.request.user.username} left a response!'
        print(link)
        html_attachment = f'<a href="{SITE_URL}{link}">Check this!</a>'
        recipient = [Post.objects.filter(pk=self.kwargs['pk']).select_related('author').only(
            'author__email')[0].author.email]
        send_mail(
            subject=subject,
            message=message,
            recipient_list=recipient,
            from_email=DEFAULT_FROM_EMAIL,
            html_message=html_attachment,
            fail_silently=True
        )
        return super().post(request, *args, **kwargs)


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostFrom
    template_name = 'forms/post.html'

    def get_success_url(self) -> str:
        return reverse_lazy('post', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = User.objects.get(id=self.request.user.id)
        return super().form_valid(form)


class ProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'


class ProfileUpdate(ProfileOwnershipVerificationMixin, UpdateView):
    form_class = UserForm
    success_url = reverse_lazy('posts')
    template_name = 'forms/profile_update.html'

    def get_object(self, **kwargs):
        return User.objects.get(pk=self.request.user.id)


class ProfileDelete(ProfileOwnershipVerificationMixin, DeleteView):
    template_name = 'forms/profile_delete.html'
    queryset = User.objects.all()
    success_url = reverse_lazy('posts')


class ResponseList(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        self.queryset = Response.objects.filter(post__author_id=self.request.user.id, approved=False).select_related(
            'post', 'author')
        return super().get_queryset()


class ResponseAcceptView(UpdateView):
    form_class = ResponseAcceptForm
    template_name = 'forms/response.html'

    def get_success_url(self) -> str:
        return reverse_lazy('post', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, **kwargs):
        my_object = Response.objects.filter(approved=False, id=self.kwargs['response_pk']).select_related('author').defer(
            'author__password',
            'author__last_login',
            'author__is_superuser',
            'author__email',
            'author__is_staff',
            'author__is_active',
            'author__date_joined',
            'post',
        )[0]
        return my_object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.filter(pk=self.kwargs['pk']).prefetch_related('category').defer('author')[0]
        return context

    def post(self, request, *args, **kwargs):
        link = reverse_lazy('post', kwargs={'pk': self.kwargs['pk']})
        subject = 'Your response has been approved!'
        message = f'{self.request.user.username} approved your response.'
        html_attachment = f'<a href="{SITE_URL}{link}">Check this!</a>'
        recipient = [Response.objects.filter(pk=self.kwargs['response_pk']).select_related('author').only(
            'author__email')[0].author.email]
        print(recipient)
        send_mail(
            subject=subject,
            message=message,
            recipient_list=recipient,
            from_email=DEFAULT_FROM_EMAIL,
            html_message=html_attachment,
            fail_silently=True,
        )
        return super().post(request, *args, **kwargs)


def logout_user(request):
    logout(request)
    return redirect('posts')


