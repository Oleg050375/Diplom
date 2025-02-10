#import PIL.Image
from django.shortcuts import render
import requests
from django.core.files.base import ContentFile
#from django.core.files import File
import os
from django.conf import settings
from .ssd import detect_objects
import cv2.dnn
#from PIL import Image
#from django.views.generic import TemplateView
#from django.http import HttpResponse
# from .forms import UserRegister
from .models import *
#from django.core.paginator import Paginator

a = None  # глобальная переменная текущего пользователя

def Home(request):  # функция обработки домашней страницы
    # формирование стартовых значений переменных
    global a
    if a == None:  # обработка случая без вошедшего пользователя
        c_us = a
        im_read_obj = None
        im_read_all = None
        prc_read = None
    else:  # обработка ситуации с вошедшим пользователем
        c_us = a.username
        im_read_obj = None
        prc_read = Prcresult.objects.all()
        im_read_all = Images.objects.filter(lord=c_us)
    page_name = 'Домашняя страница'
    proc_name = None
    del_name = None
    # обработка запроса
    if request.method == 'POST':
        proc_name = request.POST.get('image')  # получение названия изображения для обработки
        del_name = request.POST.get('delete')  # получение названия изображения для удаления
        if proc_name:
            # обработка изображения
            im_path = os.path.join(settings.BASE_DIR, f'media/{proc_name}')  # абс. путь до обрабатываемого файла
            prc = detect_objects(im_path)  # обработка изображения
            print(prc[0])
            # сохранение результатов
            prc_im_path_otn = f'/media/{proc_name}_prc.jpg'
            prc_im_path = os.path.join(settings.BASE_DIR, f'media/{proc_name}_prc.jpg')  # путь/имя
            cv2.imwrite(prc_im_path, prc[1])  # сохранение изображения
            Images.objects.filter(image_name=proc_name).update(status=prc[0], prc_path=prc_im_path_otn)  # запись рез-ов в БД
            for i in prc[0]:
                Prcresult.objects.create(prc_image_name=f'{proc_name}', prc_status=i)
        else:
            # удаление изображения
            im_del = Images.objects.get(image_name=del_name)  # чтение удаляемой записи из тб изображений
            prc_im_del = Prcresult.objects.filter(prc_image_name=del_name)  # чтение удаляемой записи из тб рез-ов
            im_path = os.getcwd() + '\media\\' + del_name  # путь/имя удаляемого исходного файла
            prc_im_path = os.path.join(settings.BASE_DIR, f'media/{del_name}_prc.jpg')  # путь/имя удаляемого prc-файла
            im_del.delete()  # удаление записи в БД
            prc_im_del.delete()  # удаление записи в БД результатов
            os.remove(im_path)  # удаление исходного изображения
            os.remove(prc_im_path)  # удаление обработанного изображения
        print(proc_name, del_name)
    context = {'page_name': page_name, 'c_us': c_us, 'prc_read': prc_read, 'im_read_all': im_read_all}
    return render(request, 'home.html', context)


def Dashboard(request):  # функция обработки страницы загрузки изображений
    global a
    if a == None:
        c_us = a
    else:
        c_us = a.username
    page_name = 'Загрузка изображений'
    im_read_obj = None
    im_status = 'не обработано'
    error = ''
    if request.method == 'POST' and a != None:
        # вынимание файла из запроса и запись его в переменную
        im_url = request.POST.get('im_url')  # получение URL изображения
        im_name = request.POST.get('im_name')  # получение имени изображения
        im = requests.get(im_url)  # загрузка изображения со страницы в инете в переменную
        # создание объекта содержимого загруженного файла и запись в БД
        im_cont = ContentFile(im.content, name=im_name)
        Images.objects.create(image=im_cont, image_name=im_name, status=im_status, lord=c_us, prc_path='Not')  # запись изображения в БД
        # чтение из БД
        im_read_obj = Images.objects.get(image_name=im_name)  # чтение записи из БД
    elif request.method == 'POST' and a == None:
        error = 'Вы не можете загрузить изображение, пока не войдёте в аккаунт'
    context = {'page_name': page_name, 'c_us': c_us, 'im_read_obj': im_read_obj, 'error': error}
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

