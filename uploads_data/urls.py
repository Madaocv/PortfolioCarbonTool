# uploads_data/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('preview/<str:model>/<int:pk>/', views.file_preview, name='file_preview'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]
