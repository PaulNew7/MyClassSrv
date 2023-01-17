import requests
import json
import logging

from django.test import TestCase
from UserControl.models import Student, Grade

HOST = 'http://localhost:8000/'
URL_Student = HOST + 'student/'
URL_Grade = HOST + 'grade/'

# Create your tests here.
class MyTest(TestCase):
    def SetUp(self):
        res = Grade.objects.create(name='哈哈')
        logging.info(f'---------初始化DB{res}')

    def test_x(self):
        res = requests.get(URL_Student)
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))



