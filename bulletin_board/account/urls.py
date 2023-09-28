from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'account'

urlpatterns = [
    path('signup/', views.BaseRegisterView.as_view(template_name='account/signup.html'), name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'),
         name='logout'),
    path('code/', views.login_with_code_view, name='code_login'),
]
