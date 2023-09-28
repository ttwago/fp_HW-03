import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.core.mail import send_mail

from .forms import BaseRegisterForm, LoginForm, CodeLoginForm
from .models import OneTimeCode


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/account/login'


def login_view(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                code = OneTimeCode.objects.create(code=random.randint(1000, 9999), user=user)
                send_mail(
                    subject='Доска объявлений: ваш одноразовый код',
                    message=f'Код: {code.code}',
                    from_email='someone.unknown@yandex.ru',
                    recipient_list=[user.email]
                )
                return redirect('/account/code')
            else:
                message = 'Invalid login'
    return render(request, 'account/login.html', context={'form': form, 'message': message})


def login_with_code_view(request):
    form = CodeLoginForm()
    message = ''
    if request.method == 'POST':
        form = CodeLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            code = form.cleaned_data['code']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                message = 'User does not exist'
                return render(request, 'account/code_login.html', context={'form': form, 'message': message})
            if OneTimeCode.objects.filter(code=code, user__username=username).exists():
                login(request, user)
                return redirect('/')
            else:
                message = 'Invalid code'
    return render(request, 'account/code_login.html', context={'form': form, 'message': message})
