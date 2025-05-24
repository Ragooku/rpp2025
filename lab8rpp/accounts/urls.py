from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('no-permission/', TemplateView.as_view(template_name='accounts/no_permission.html'), name='no-permission'),
]