import PIL.Image
import cv2.dnn
import requests
import os
from PIL import Image
#from models import *

# https://ru.freepik.com/

url = 'https://img.freepik.com/premium-photo/medium-shot-woman-living-farmhouse_23-2150621719.jpg?w=1060'
url2 = 'https://img.freepik.com/free-photo/adorable-kitty-with-monochrome-wall-her_23-2148955146.jpg?ga=GA1.1.1787463696.1736662973&semt=ais_hybrid'

#os.remove('/media/Маша')

#a = PIL.Image.open('media/Маша')

#print(os.getcwd())

def detect_objects(image_path):
    prototxt = ''  # конфиг модели
    model = ''  # весовые кэффициенты
    net = cv2.dnn.readNetFromCaffe(prototxt, model)  # загрузка модели с использованием библиотеки openCV
    CLASSES = []  # список распознаваемых классов
    image = cv2.imread(image_path)  # загрузка изображения в переменную
    blob = cv2.dnn.blobFromImage(image, 0.007843, (300,300), 127.5)  # преобр-ие из-я в формат blob
    net.setInput(blob)  # подаём изображение на вход нейросети
    detections = net.forward()
