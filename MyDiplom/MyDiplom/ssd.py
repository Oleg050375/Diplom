import cv2.dnn
import os

def detect_objects(image_path):  # функция распознавания объектов на изображении

    # адреса расположения модели и весовых коэффициентов
    prototxt = 'object_detection\\MobileNetSSD_deploy.prototxt'
    model = 'object_detection\\mobilenet_iter_73000.caffemodel'

    # подготовка модели к работе
    net = cv2.dnn.readNetFromCaffe(prototxt, model)  # загрузка модели с использованием библиотеки openCV
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair",
               "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa",
               "train", "tvmonitor"]  # список распознаваемых классов

    # подготовка изображения
    image = cv2.imread(image_path)  # загрузка изображения в переменную
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300,300)), 0.007843, (300,300), 127.5)  # преобр-ие из-я в формат blob

    # работа модели (распознавание объектов)
    net.setInput(blob)  # подаём изображение на вход нейросети
    detections = net.forward()  # вероятно, запуск модели и сохранение результатов в переменную
    print(detections.shape)
    for i in range(100):
        confidence = detections[0,0,i,2]
        if confidence > 0.2:
            print(i)
            print(confidence)

    # обработка результатов работы модели
    results = []  # результат распознавания


detect_objects('000001.jpg')