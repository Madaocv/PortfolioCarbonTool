# calculations_and_pages/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.holdings, name='holdings'),  # Головна сторінка
    path('api/calculate-chart-data/', views.calculate_chart_data, name='calculate_chart_data'),
    # path('calculate/', views.calculate, name='calculate'),  # Сторінка обрахунків
    # Додаткові маршрути
]
