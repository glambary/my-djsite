import dotenv
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *
from my_travel_site.settings import GMAIL_PASSWORD


class AddTourForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dep'].empty_label = 'Город отправления не выбран'

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title

    class Meta:
        model = Travel
        # fields = '__all__'
        fields = ['title', 'slug', 'content', 'photo','is_published', 'price', 'duration', 'dep']
        '''Атрибут model как раз устанавливает связь формы с моделью Travel
          свойство fields – определяет поля для отображения в форме.
          Значение __all__ говорит показывать все поля, кроме тех, что заполняются автоматически.
          Получилась форма, только без полей time_create и time_update, так как они наполняются без участия пользователя.'''
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Сообщение')
    captcha = CaptchaField(label='Введите код')

    def send_email(self):
        import smtplib
        from email.mime.text import MIMEText
        import os

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        sender = "glam.sendler@gmail.com"

        # PASSWORDS
        password = GMAIL_PASSWORD

        try:
            server.login(sender, password)

            message = MIMEText(', '.join([f'{key}: {value}' for key, value in self.cleaned_data.items() if key != 'captcha']))
            message['Subject'] = 'My-Travel-site!'

            server.sendmail(sender, "glambary@yandex.ru", message.as_string())
            print('the message was sent successfully')
        except Exception as err:
            print(f'{err}. Ошибка в send_email')




'''
# форма "не связанная" с моделью
class AddTourForm(forms.Form):
    title = forms.CharField(max_length=255, label='Заголовок')
    slug = forms.SlugField(max_length=255, label='URL')
    content = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        label='Контент'
    )
    is_published = forms.BooleanField(label='Публикация', required=False, initial=True)
    price = forms.DecimalField(max_digits=10, decimal_places=2, label='Цена')
    duration = forms.CharField(max_length=50, label='Продолжительность')
    dep = forms.ModelChoiceField(queryset=Departure.objects.all(), label='Город отправления', empty_label="Город отправления не выбран")
'''
