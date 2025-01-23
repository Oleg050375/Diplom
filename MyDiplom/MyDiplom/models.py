from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class Images(models.Model):
    image = models.ImageField()
    image_name = models.CharField(max_length=30, default=None)
    lord = models.CharField(max_length=30, default=None)
    status = models.CharField(max_length=30, default=None)

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
