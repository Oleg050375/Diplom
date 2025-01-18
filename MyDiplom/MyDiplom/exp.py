import requests
from PIL import Image
#from models import *

# https://ru.freepik.com/

url = 'https://img.freepik.com/premium-photo/medium-shot-woman-living-farmhouse_23-2150621719.jpg?w=1060'
url2 = 'https://img.freepik.com/free-photo/adorable-kitty-with-monochrome-wall-her_23-2148955146.jpg?ga=GA1.1.1787463696.1736662973&semt=ais_hybrid'

#fl = open('img1', 'wb')

#a = requests.get(url2)

#Images.objects.create(image=a.content)

#fl.write(a.content)

n = Images.objects.get(id=1)

imp = Image.open('img1')

imp.show()