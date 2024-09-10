from django.urls import path
from . import views

urlpatterns = [
    path('preview/<str:model>/<int:pk>/', views.file_preview, name='file_preview'),
]
