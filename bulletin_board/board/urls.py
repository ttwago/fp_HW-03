from django.urls import path

from . import views

app_name = 'board'

urlpatterns = [
    path('', views.PostList.as_view(), name="post_list"),
    path('create/', views.PostCreate.as_view(), name="create_post"),
    path('<int:pk>/', views.PostDetail.as_view(), name="post_detail"),
    path('<int:pk>/update/', views.PostUpdate.as_view(), name="update_post"),
    path('<int:pk>/respond/', views.ResponseCreate.as_view(), name="respond"),
    path('responses/', views.ResponseList.as_view(), name="response_list"),
    path('responses/<int:pk>/', views.ResponseDetail.as_view(), name="response_detail"),
    path('responses/<int:pk>/accept/', views.accept_response, name="accept"),
    path('responses/<int:pk>/deny/', views.deny_response, name="deny"),
    path('success/', views.SuccessView.as_view(), name="success"),
]