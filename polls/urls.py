from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'polls'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='polls/login.html'), name='login'),
    path('', views.index, name='index'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('<int:poll_id>/vote/', views.vote, name='vote'),
    path('poll/<int:poll_id>/results/', views.poll_results, name='results'),
    path('create/', views.create_poll, name='create_poll'),
    path('<int:poll_id>/edit/', views.edit_poll, name='edit_poll'),
    path('<int:poll_id>/delete/', views.delete_poll, name='delete_poll'),
]