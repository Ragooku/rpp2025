from django.urls import path
from .views import (
    MachineListView, MachineDetailView,
    MachineCreateView, MachineUpdateView,
    MachineDeleteView, ReadingCreateView, ReadingDeleteView
)

urlpatterns = [
    path('', MachineListView.as_view(), name='machine-list'),
    path('<int:pk>/', MachineDetailView.as_view(), name='machine-detail'),
    path('new/', MachineCreateView.as_view(), name='machine-create'),
    path('<int:pk>/edit/', MachineUpdateView.as_view(), name='machine-update'),
    path('<int:pk>/delete/', MachineDeleteView.as_view(), name='machine-delete'),
    path('<int:machine_pk>/readings/add/', ReadingCreateView.as_view(), name='reading-add'),
    path('readings/<int:pk>/delete/', ReadingDeleteView.as_view(), name='reading-delete'),
]