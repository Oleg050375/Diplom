import cv2.dnn
import os
from django.conf import settings
from django.urls import reverse

def detect_objects(image_path):  # функция распознавания объектов на изображении

    # адреса расположения модели и весовых коэффициентов
    prototxt = os.path.join(settings.BASE_DIR, 'MyDiplom/object_detection/deploy.prototxt')
    model = os.path.join(settings.BASE_DIR, 'MyDiplom/object_detection/mobilenet_iter_73000.caffemodel')
    #model = 'object_detection\\mobilenet_iter_73000.caffemodel'

    # подготовка модели к работе
    net = cv2.dnn.readNetFromCaffe(prototxt, model)  # загрузка модели с использованием библиотеки openCV
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair",
               "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa",
               "train", "tvmonitor"]  # список распознаваемых классов
    results = []  # заготовка результатов распознавания

    # подготовка изображения
    image = cv2.imread(image_path)  # загрузка изображения в переменную
    (h, w) = image.shape[0:2]  # определение размеров исходного изображения
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300,300)), 0.007843, (300,300), 127.5)  # преобр-ие из-я в формат blob

    # работа модели (распознавание объектов)
    net.setInput(blob)  # подаём изображение на вход нейросети
    detections = net.forward()  # запуск модели и сохранение результатов в переменную

    for i in range(100):  # перебор обнаруженных классов

        confidence = detections[0,0,i,2]  # чтение точности распознавания

        if confidence > 0.2:  # фильтрация по точности обнаружения

            class_id = CLASSES[int(detections[0, 0, i, 1])]  # чтение класса распознанного объекта

            # формирование координат области обнаружения
            y_min = int(detections[0,0,i,3] * h)
            x_min = int(detections[0,0,i,4] * w)
            y_max = int(detections[0,0,i,5] * h)
            x_max = int(detections[0,0,i,6] * w)

            # рисование рамки области обнаружения на исходном изображении
            color = (0, 255, 0)  # задание цвета рамки
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)  # нанесение рамки

            # сохранение результата
            #results.append({'class': class_id, 'confidence': confidence, 'box': (x_min, y_min, x_max, y_max)})
            results.append({'class': class_id, 'confidence': confidence})

    file_name = os.path.basename(image_path) + '_prc'
    print(file_name)
    #cv2.imwrite(f'{file_name}.jpg', image)

    return results, image


# TEST ----------------------------------------------------------------------------------------------------------------


"""
im_path = os.path.join(settings.BASE_DIR, 'media/Man')
print(im_path)

#detect_objects('000001.jpg')  # мужик с собакой
a = detect_objects(im_path)
print(a[0])  # самолёт
#cv2.imwrite('im_prc.jpg', a[1])
#detect_objects('000456.jpg')  # автобус
#detect_objects('000542.jpg')  # кошка
#detect_objects('001150.jpg')  # собака и люди
#detect_objects('001763.jpg')  # собака и кот
#detect_objects('004545.jpg')  # много всего
"""