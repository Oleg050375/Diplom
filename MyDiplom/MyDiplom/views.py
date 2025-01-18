from django.shortcuts import render
import requests
from PIL import Image
from django.views.generic import TemplateView
from django.http import HttpResponse
# from .forms import UserRegister
from .models import *
from django.core.paginator import Paginator

a = None  # глобальная переменная текущего пользователя

def Home(request):  # функция обработки домашней страницы
    global a
    if a == None:
        c_us = a
    else:
        c_us = a.username
    page_name = 'Домашняя страница'
    context = {'page_name': page_name, 'c_us': c_us}
    return render(request, 'home.html', context)


def Dashboard(request):
    global a
    if a == None:
        c_us = a
    else:
        c_us = a.username
    page_name = 'Загрузка изображений'
    if request.method == 'POST':
        # вынимание файла из запроса и запись его в переменную
        im_url = request.POST.get('im_url')  # получение URL изображения
        im_name = request.POST.get('im_name')  # получение имени изображения
        im = requests.get(im_url)  # загрузка изображения со страницы в инете в переменную
        # создание фйла временного хранения и запись туда изображения
        im_f = open('img1', 'wb')  # открытие файла временного хранения изображения
        im_f.write(im.content)  # запись загруженного изображения в файл временного хранения
        im_f.close()
        # чтение изображения из файла временного хранения, запись в БД и закрытие файла временного хр-я
        im_f = open('img1', 'rb')
        im_f_r = im_f.read()  # чтение содержимого файла временного хранения в переменную
        Images.objects.create(image=im_f_r, image_name=im_name)  # запись изображения в БД
        im_f.close()
    context = {'page_name': page_name, 'c_us': c_us}
    return render(request, 'dashboard.html', context)


def Login(request):  # функция обработки страницы входа
    global a
    if a == None:
        c_us = a
    else:
        c_us = a.username
    page_name = 'Вход'
    txt = 'Введите свои данные'
    error = ' '
    hello = ' '
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        u_s = User.objects.filter(username=username)  # формирование списка записей с именем пользователя
        if len(u_s) == 0:  # проверка списка на пустоту
            error = 'Пользователь не найден. Зарегистрируйтесь.'
        else:
            error = 'Пароль неверный.'
            for i in u_s:  # цикл поиска записи с нужным паролем
                if i.password == password:
                    hello = f'Приветствуем, {username}!'
                    error = ''
                    a = i
                    c_us = a.username
    context = {'txt': txt, 'error': error, 'hello': hello, 'page_name': page_name, 'c_us': c_us}
    return render(request, 'login.html', context)


def Logout(request):  # функция обработки страницы выхода
    global a
    if a == None:
        c_us = a
    else:
        c_us = a.username
    page_name = 'Выход'
    if request.method == 'POST' and request.POST.get('token') == 'выход':  # обработка запроса на выход
        a = None  # сброс текущего пользователя
        c_us = a
    context = {'page_name': page_name, 'c_us': c_us}
    return render(request, 'logout.html', context)


def Registration(request):  # функция обработки страницы регистрации
    global a
    if a == None:
        c_us = a
    else:
        c_us = a.username
    page_name = 'Регистрация'
    txt = 'Введите свои данные'
    error = ' '
    hello = ' '
    if request.method == 'POST':  # проверка типа запроса
        username = request.POST.get('username')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        for i in username:  # проверка на состав символов логина
            if i.isalnum() or i in '@,+-_':
                continue
            else:
                error = 'Неверный состав символов логина'
                break
        if len(username) >= 20:  # проверка на длину логина
            error = 'Длина логина больше 20 символов'
        elif error != ' ':
            pass
        else:
            if password == repeat_password:  # проверка на совпадение паролей
                User.objects.create(username=username, password=password)  # добавление пользователя в БД
                hello = f'Пользователь {username} зарегистрирован.'
            else:
                error = 'Пароли не совпадают'
    context = {'txt': txt, 'error': error, 'hello': hello, 'page_name': page_name, 'c_us': c_us}
    return render(request, 'registration.html', context)
