from django.shortcuts import render, get_object_or_404, redirect
# from .models import CompanyFile, PortfolioFile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SimpleRegistrationForm, SimpleLoginForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = SimpleRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('holdings')  # Змінити на вашу домашню сторінку
    else:
        form = SimpleRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = SimpleLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('holdings')  # Перенаправляємо після успішного логіну
            else:
                messages.error(request, 'Invalid username or password.')  # Повідомлення про помилку логіну
        else:
            # Додаємо всі помилки форми у повідомлення
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SimpleLoginForm()
    return render(request, 'login.html', {'form': form})
