# calculations_and_pages/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.holdings, name='holdings'),  # Головна сторінка
    path('portfolio', views.portfolio, name='portfolio'),
    path('createportfolio', views.createportfolio, name='createportfolio'),
    path('api/calculate-chart-data/', views.calculate_chart_data, name='calculate_chart_data'),
    path('api/calculate-portfolio-data/', views.calculate_portfolio_data, name='calculate_portfolio_data'),
    # path('calculate/', views.calculate, name='calculate'),  # Сторінка обрахунків
    # Додаткові маршрути
]
