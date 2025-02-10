from django.db import models


class User(models.Model):  # таблица пользователей
    username = models.CharField(max_length=20)  # имя пользователя
    password = models.CharField(max_length=20)  # пароль пользователя


class Images(models.Model):  # таблица изображений
    image = models.ImageField(default=None)  # исходное изображение
    prc_path = models.CharField(max_length=100, default=None)  # название изображения
    image_name = models.CharField(max_length=30, default=None)  # название изображения
    lord = models.CharField(max_length=30, default=None)  # владелец изображения
    status = models.CharField(max_length=30, default=None)  # результат распознавания

class Prcresult(models.Model):  # таблица результатов обработки
    prc_image_name = models.CharField(max_length=30, default=None)  # название обработанного изображения
    prc_status = models.CharField(max_length=30, default=None)  # результат распознавания

"""
class Game(models.Model):
    title = models.CharField(max_length=20)
    cost = models.DecimalField(decimal_places=2, max_digits=5)
    size = models.DecimalField(decimal_places=3, max_digits=5)
    description = models.TextField()
    age_limited = models.BooleanField(default=False)
    buyer = models.ManyToManyField(Buyer)


class News(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    date = models.DateField()
"""
