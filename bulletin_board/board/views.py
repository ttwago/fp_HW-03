from django.views import generic
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail

from .models import Post, User, Response
from .forms import PostCreateForm, ResponseCreateForm


class PostList(generic.ListView):
    model = Post
    ordering = '-creation_time'
    template_name = 'board/post_list.html'
    context_object_name = 'post_list'


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'board/post_detail.html'


class PostCreate(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'board/post_edit.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = User.objects.get(id=self.request.user.id)
        self.object.save()
        result = super().form_valid(form)
        return result


class PostUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostCreateForm

    def get_template_names(self):
        post = self.get_object()
        if post.user == self.request.user:
            self.template_name = 'board/post_edit.html'
            return self.template_name
        else:
            raise PermissionDenied


class ResponseList(LoginRequiredMixin, generic.ListView):
    model = Response
    template_name = 'board/response_list.html'
    context_object_name = 'response_list'
    ordering = '-creation_time'

    def get_queryset(self):
        queryset = Response.objects.filter(post__user=self.request.user)
        return queryset


class ResponseDetail(LoginRequiredMixin, generic.DetailView):
    model = Response

    def get_template_names(self):
        response = self.get_object()
        if response.post.user == self.request.user:
            self.template_name = 'board/response_detail.html'
            return self.template_name
        else:
            raise PermissionDenied


class ResponseCreate(LoginRequiredMixin, generic.CreateView):
    model = Response
    template_name = 'board/response_create.html'
    form_class = ResponseCreateForm
    success_url = '/success/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = User.objects.get(id=self.request.user.id)
        self.object.post = Post.objects.get(id=self.kwargs['pk'])
        self.object.save()
        result = super().form_valid(form)
        send_mail(
            subject=f'Получен отклик на пост "{self.object.post.title}"',
            message=f'Отклик: "{self.object.comment}"',
            from_email='aidigo.grigorjev@yandex.ru',
            recipient_list=[self.object.post.user.email]
        )
        return result


class SuccessView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'board/success.html'


@login_required()
def accept_response(request, pk):
    response = Response.objects.get(pk=pk)
    response.status = 'Y'
    response.save()
    send_mail(
        subject=f'Доска объявлений: отлик принят',
        message=f'Ваш отклик на пост "{response.post.title}" принят',
        from_email='someone.unknown@yandex.ru',
        recipient_list=[response.user.email]
    )
    return HttpResponseRedirect(reverse('response_list'))


@login_required()
def deny_response(request, pk):
    response = Response.objects.get(pk=pk)
    response.status = 'N'
    response.save()
    return HttpResponseRedirect(reverse('response_list'))
