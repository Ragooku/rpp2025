from django.urls import path
from . import views

urlpatterns = [
    path('', views.MachineListView.as_view(), name='machine-list'),
    path('<int:pk>/', views.MachineDetailView.as_view(), name='machine-detail'),
    path('create/', views.MachineCreateView.as_view(), name='machine-create'),
    path('<int:pk>/update/', views.MachineUpdateView.as_view(), name='machine-update'),
    path('<int:pk>/delete/', views.MachineDeleteView.as_view(), name='machine-delete'),
]