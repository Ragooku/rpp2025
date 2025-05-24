from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import RegisterForm, LoginForm
from .models import Role, UserProfile

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('machine-list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')

                # Перенаправляем в зависимости от роли
                if hasattr(user, 'profile') and user.profile.role:
                    return redirect_by_role(request, user.profile.role.name)
                return redirect('machine-list')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('machine-list')


def redirect_by_role(request, role_name):
    """Перенаправление пользователя в зависимости от роли"""
    if role_name == 'Начальник':
        return redirect('machine-list')  # Или другой специальный URL
    elif role_name == 'Оператор':
        return redirect('machine-list')
    return redirect('machine-list')


def check_role_required(role_name):
    """Декоратор для проверки ролей"""

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if not hasattr(request.user, 'profile') or not request.user.profile.role:
                raise PermissionDenied("У вас нет назначенной роли")

            if request.user.profile.role.name != role_name:
                raise PermissionDenied("Недостаточно прав")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def any_role_required(role_names):
    """Декоратор для проверки нескольких ролей"""

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')

            if not hasattr(request.user, 'profile') or not request.user.profile.role:
                raise PermissionDenied("У вас нет назначенной роли")

            if request.user.profile.role.name not in role_names:
                raise PermissionDenied("Недостаточно прав")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator