import random
import time
import requests
import json
import datetime

from django.test import TestCase
from UserControl.models import Student, Grade

HOST = 'http://localhost:8000/'
URL_Student = HOST + 'students/'
URL_Grade = HOST + 'grades/'

# Create your tests here.
class MyTest(TestCase):
    new_grade = None
    new_stu = None
    
    # def SetUp(self):
    #     print('...>>>>>>>init')
    #     res = Grade.objects.create(name='哈哈')
    #     print(f'---------init-DB{res}')
    def test_grade_api(self):
        # 增
        # for i in range(10):
        # for i in range(1):
        #     self.t_post_grade()
        # #改
        # self.t_put_grade(self.new_grade['id'])
        # # self.t_put_grade(34) # debug
        # # 查单个
        # self.t_get_grade(self.new_grade['id'])
        # # 查前10个
        # self.t_get_grades()
        # 查前指定名字
        # self.t_get_grades('ddd')
        # self.t_get_grades('一年级二班')
        # # # 删最后一个
        # # # self.t_delete_grade(self.new_grade['id'])
        pass

    def test_stu_api(self):
        # 增
        # for i in range(10):
        # for i in range(1):
        #     self.t_post_stuents()
        # # 改
        # self.t_patch_student(self.new_grade['id'])
        # # self.t_put_grade(34) # debug
        # # # 查单个
        # self.t_get_student(self.new_grade['id'])
        # # # 查前10个
        # self.t_get_students()

        # 根据名字查询
        self.t_get_students('小米')
        # # # 删最后一个
        pass

    def t_post_stuents(self):
        print('create_stu')
        params = {
            'name': f'名字{datetime.datetime.now()}',
            'code': int(str(time.time()).split('.')[1]),
            'gender': random.randint(1, 3),
            'grade': random.randint(1, 3)
        }
        res = requests.post(URL_Student, json=params)
        # if res.status_code >300:
        #     print(res.content)
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))
        self.new_grade = res.json()
        self.assertEqual(res.status_code, 201)

    def t_get_students(self, name=None):
        print('stu_list')
        if name:
            res = requests.get(URL_Student, params={'name': name})
        else:
            res = requests.get(URL_Student)
        self.handler_error(res)
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))

    def t_get_student(self, pk=1):
        print(f'get_student--------{pk}')
        res = requests.get(URL_Student + f'{pk}/')
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))

    def t_patch_student(self, pk=1):
        print('put_student')
        params = {'name': f'新名字{datetime.datetime.now()}',
                  'grade': 21}
        res = requests.patch(URL_Student + f'{pk}/', json=params)
        if res.status_code >300:
            with open('./error.html','wb') as f:
                f.write(res.content)
            # print(res.content)
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))

    # def t_patch_student(self):
    #     print('stu_patch')
    #
    #     res = requests.put(URL_Student, json=)
    #     print(json.dumps(res.json(), indent=4, ensure_ascii=False))
    def handler_error(self, res):
        if res.status_code >300:
            with open('./error.html','wb') as f:
                f.write(res.content)

    def t_post_grade(self):
        print('create_grade')
        params = {'name': f'名字{datetime.datetime.now()}'}
        res = requests.post(URL_Grade, json=params)
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))
        self.new_grade = res.json()
        self.assertEqual(res.status_code, 201)

    def t_get_grades(self, name=None):
        print('grade_list')
        if name:
            res = requests.get(URL_Grade, params={'name':name})
        else:
            res = requests.get(URL_Grade)
        self.handler_error(res)
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))

    def t_get_grade(self, pk=1):
        print(f'get_grade--------{pk}')
        res = requests.get(URL_Grade+f'{pk}/')
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))

    def t_put_grade(self, pk=1):
        print('put_grade')
        params = {'name': f'新名字{datetime.datetime.now()}'}
        res = requests.put(URL_Grade+f'{pk}/', json=params)
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))

    def t_delete_grade(self, pk=1):
        print(f'del_grade-----------{pk}')
        # params = {'name': f'新名字{datetime.datetime.now()}'}
        res = requests.delete(URL_Grade+f'{pk}/')
        print(json.dumps(res.status_code, indent=4, ensure_ascii=False))
        self.assertEqual(res.status_code, 204)


