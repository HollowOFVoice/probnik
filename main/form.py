from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from main.models import Request


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput,label='Пароль')

    def clean(self):
        cleaned_data = super(UserLoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username and password:
            raise ValidationError("Пароль или логин не могут быть пустыми")

        user = authenticate(username=username, password=password)
        if  user is None:
            raise ValidationError("Неверный логин или пароль.")

        return cleaned_data

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput,label='Пароль')
    class Meta:
        model = User
        fields = ('username', 'password', 'email','first_name', 'last_name')
        labels = {
            'username':'имя пользователя',
            'email':'Почта',
            'first_name':'Фамилия',
            'last_name':'Отчество'
        }
    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('password')

        # Проверяем, что пароли совпадают
        if password and confirm_password and password != confirm_password:  # Если пароли не совпадают
            raise ValidationError("Пароли не совпадают.")  # Выбрасываем ошибку валидации

        return cleaned_data


class RequestForm(forms.ModelForm):  # Определяем форму для создания заявки
    class Meta:  # Вложенный класс Meta для настройки формы
        model = Request  # Указываем модель Request
        fields = ['address', 'service', 'desired_date', 'payment_type']  # Определяем поля формы
        labels = {  # Задаем метки для полей формы
            'address': 'Адрес',
            'service': 'Услуга',
            'desired_date': 'Дата и время',
            'payment_type': 'Тип оплаты',
        }
        widgets = {  # Настраиваем виджеты для полей формы
            'desired_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Поле для выбора даты и времени
        }

    def clean(self):  # Переопределяем метод clean для валидации данных формы
        cleaned_data = super().clean()  # Получаем очищенные данные из родительского метода
        address = cleaned_data.get('address')  # Получаем адрес из очищенных данных

        # Валидация, что все необходимые поля заполнены
        if not address:  # Если адрес пустой
            raise ValidationError("Адрес не может быть пустым.")  # Выбрасываем ошибку валидации

        return cleaned_data  # Возвращаем очищенные данные
