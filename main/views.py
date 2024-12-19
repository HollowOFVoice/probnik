from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

from main.form import UserRegistrationForm, UserLoginForm, RequestForm


# Create your views here.
def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)  # Аутентификация пользователя

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None,
                               "Неверный логин или пароль.")  # Добавляем ошибку, если не удалось аутентифицировать пользователя
    else:
        form = UserLoginForm()  # Создаем пустую форму для входа

    return render(request, 'login.html', {'form': form})  # Рендерим шаблон входа с формой

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect("login")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})
def home(request):
    return render(request, 'home.html')

@login_required  # Декоратор, который требует аутентификации для доступа к функции
def create_request(request):  # Функция для создания новой заявки
    if request.method == 'POST':  # Проверяем, был ли отправлен POST-запрос
        form = RequestForm(request.POST)  # Создаем экземпляр формы с данными из запроса
        if form.is_valid():  # Проверяем, валидна ли форма
            new_request = form.save(commit=False)  # Создаем заявку, но не сохраняем ее сразу
            new_request.user = request.user  # Связываем заявку с текущим пользователем
            new_request.save()  # Сохраняем заявку в базе данных
            return redirect('home')  # Перенаправляем на главную страницу после успешной подачи заявки
    else:
        form = RequestForm()  # Создаем пустую форму для заявки

    return render(request, 'create_request.html', {'form': form})  # Рендерим шаблон создания заявки с формой



