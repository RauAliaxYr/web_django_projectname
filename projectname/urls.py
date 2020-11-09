from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Обработчики действий со статьями.
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('edit_event', views.edit_event, name='edit_event'),
    path('delete_event', views.delete_event, name='delete_event'),

]
