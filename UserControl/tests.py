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
        print('...>>>>>>>init')
        res = Grade.objects.create(name='哈哈')
        print(f'---------init-DB{res}')

    def test_get_students(self):
        print('stu_list')
        res = requests.get(URL_Student)
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))

    def test_put_students(self):
        print('stu_edit')

        # res = requests.put(URL_Student, json=)
        # print(json.dumps(res.json(), indent=4, ensure_ascii=False))

    def test_get_grades(self):
        print('grade_list')
        res = requests.get(URL_Grade)
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))


