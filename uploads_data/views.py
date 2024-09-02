# uploads_data/views.py
from django.shortcuts import render, get_object_or_404, redirect
import pandas as pd
from .models import CompanyFile, PortfolioFile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SimpleRegistrationForm


@login_required
def file_preview(request, pk, model):
    if model == 'companyfile':
        file_instance = get_object_or_404(CompanyFile, pk=pk)
        df_instance = file_instance.data_frame
    elif model == 'portfoliofile':
        file_instance = get_object_or_404(PortfolioFile, pk=pk)
        df_instance = file_instance.data_frame

    # Завантажуємо DataFrame із бази даних
    if df_instance:
        df = df_instance.get_data_frame()

        # Конвертуємо DataFrame у HTML для перегляду
        preview_html = df.to_html()
    else:
        preview_html = "<p>No data available for this file.</p>"

    return render(request, 'uploads_data/preview.html', {'preview_html': preview_html})


def register(request):
    if request.method == 'POST':
        form = SimpleRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Змінити на вашу домашню сторінку
    else:
        form = SimpleRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('holdings')  # Змінити на вашу домашню сторінку
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})