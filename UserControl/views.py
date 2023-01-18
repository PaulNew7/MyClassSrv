import json
import logging
import time

from django.shortcuts import render
from django.http.response import HttpResponseForbidden
from django.core.cache import cache
from rest_framework import viewsets

from UserControl.models import Student, Grade
from UserControl.serializers import StudentSerializer, GradeSerializer


# TODO 拆离view层
# TODO 删除学生/班级时的缓存联动
class CacheUtils():
    '''

    命名空间: 'cache__'+app名称+‘__’

    学生
    key: 'cache__UserControl__stuInfo'
    value:    {
            id:{
                name:xx,
                code:xx,
                gender:xx,
                grade_id: xx
            }
        }

    key: 'cache__UserControl__stuMap'
    value:
        {name: id}

    班级
    key: 'cache__UserControl__gradeInfo'
    value:
        {
            name: {学生id，...}
        }

    key: 'cache__UserControl__gradeMap'
    value:
        {id: name}
    '''
    def __init__(self):
        self.key_gradeMap = 'cache__UserControl__gradeMap'
        self.key_gradeInfo = 'cache__UserControl__gradeInfo'
        self.key_stuMap = 'cache__UserControl__stuMap'
        self.key_stuInfo = 'cache__UserControl__stuInfo'

    def lock(self, key, try_times=3, expire=3):
        '''
        超时锁
        :param key: 区分不同锁
        :param try_times: 重试时间
        :param expire: 锁超时时间
        :return: bool 是否成功
        '''
        lock_key = f'lock__{key}'
        for i in range(try_times):
            logging.info(f'try_{i+1}_get_lock__{lock_key}')
            lock = cache.get(lock_key)
            if not lock:
                cache.set(lock_key,1,expire)
                return True
            else:
                time.sleep(1)
        logging.error(f'try_{i + 1}_fail_to_lock__{lock_key}')
        return False

    def unlock(self, key):
        '''
        释放锁
        :param key:
        :return:
        '''
        lock_key = f'lock__{key}'
        logging.info(f'release_lock__{lock_key}')
        cache.delete(lock_key)

    def get_or_init(self, key, default):
        raw = cache.get(key) or default
        # if raw is None:
        #     logging.warning(f'init_cache__{key}__{default}')
        #     if self.lock(key):
        #         cache.set(key, default)
        #         self.unlock(key)
        #     else:
        #         raise Exception('fail to update cache')
        #     raw = json.dumps(default)
        if isinstance(raw, str):
            raw = json.loads(raw)
        return raw

    def set(self, key, val):
        logging.info(f'----update-cache:{key}:{val}')
        if isinstance(val, set):
            val = list(val)
        cache.set(key, json.dumps(val))

    def get_multi_stu_info(self, stu_id_list):
        '''
        根据stu_id批量查询cache，不存在查库并更新cache
        :param stu_id_list:
        :return: [
            {
                id:xx,
                name:xx,
                code:xx,
                gender:xx,
                grade_id: xx
            }
        ]
        '''
        result = []
        if not stu_id_list:
            return result

        not_find_stu_id_list = set()
        data = self.get_or_init(self.key_stuInfo, {})
        logging.info(f'{self.key_stuInfo}:---{data}')
        for stu_id in stu_id_list:
            info = data.get(str(stu_id))
            if not info:
                not_find_stu_id_list.add(stu_id)
            else:
                result.append(info)

        # 批量查询未缓存的stu
        if not_find_stu_id_list:
            logging.info(f"now_query_stu:{not_find_stu_id_list}")
            stu_list = Student.objects.filter(id__in=not_find_stu_id_list)

            # 更新cache
            for stu in stu_list:
                self.update_stu_info(stu.id, stu.name, stu.code, stu.gender, stu.grade_id, stu.grade.name)
                result.append({
                    'name': stu.name,
                    'code': stu.code,
                    'gender': stu.gender,
                    'grade_id': stu.grade_id
                })

        return result

    def update_stu_info(self, stu_id, name, code, gender, grade_id, grade_name):
        '''
        更新学生信息, 学生映射和班级学生映射cache
        幂等操作，新增修改皆可使用。
        :param stu_id:
        :param name:
        :param code:
        :param gender:
        :param grade_id:
        :param grade_name:
        :return:
        '''
        # 更新学生信息cache
        data = self.get_or_init(self.key_stuInfo, {})
        logging.info(f'{self.key_stuInfo}:---{data}')
        if self.lock(self.key_stuInfo):
            data[stu_id] = {
                'id': stu_id,
                'name': name,
                'code': code,
                'gender': gender,
                'grade_id': grade_id
            }
            self.set(self.key_stuInfo, data)
            # 释放锁
            self.unlock(self.key_stuInfo)
        else:
            raise Exception('fail to update cache')

        # 更新学生映射cache
        data_map = self.get_or_init(self.key_stuMap, {})
        if self.lock(self.key_stuMap):
            data_map[name] = stu_id
            self.set(self.key_stuMap, data_map)
            # 释放锁
            self.unlock(self.key_stuMap)
        else:
            raise Exception('fail to update cache')

        # 更新班级学生映射cache
        # self.add_grade_info(grade_name, {stu_id}) # 不能单个更新，可能出现不一致
        self.update_grade_info(grade_name)

    def update_grade_info(self, name):
        '''
        批量更新班级学生映射
        :param name:
        :return: [stu_id,...]
        '''
        data = self.get_or_init(self.key_gradeInfo, {})
        logging.info(f'{self.key_gradeInfo}:---{data}')
        if self.lock(self.key_gradeInfo):
            l_stu_id = Grade.objects.get(name=name).student_set.values_list('id')
            data[name] = [i[0] for i in list(l_stu_id)]
            self.set(self.key_gradeInfo, data)
            # 释放锁
            self.unlock(self.key_gradeInfo)
            return l_stu_id
        else:
            raise Exception('fail to update cache')

    def add_grade_info(self, name, stu_id_set):
        '''
        批量更新班级学生映射
        :param name:
        :param stu_id_set:
        :return:
        '''
        data = self.get_or_init(self.key_gradeInfo, {})
        logging.info(f'{self.key_gradeInfo}:---{data}')
        if self.lock(self.key_gradeInfo):
            if name not in data:
                data[name] = set()
            data[name].update(stu_id_set)
            self.set(self.key_gradeInfo, data)
            # 释放锁
            self.unlock(self.key_gradeInfo)
        else:
            raise Exception('fail to update cache')

    def update_grade_map(self, name, pk):
        data = self.get_or_init(self.key_gradeMap, {})
        if self.lock(self.key_gradeMap):
            data[pk] = name
            self.set(self.key_gradeMap, data)
            # 释放锁
            self.unlock(self.key_gradeMap)
        else:
            raise Exception('fail to update cache')

    def get_grad_name_by_id(self, pk):
        '''

        :param pk:
        :return:
        '''
        data = self.get_or_init(self.key_gradeMap, {})
        name = data.get(pk)

        # 无缓存，则更新
        if not name:
            name = Grade.objects.get(id=pk).values('name')[0]
            self.update_grade_map(name, pk)

        return name

    def read_grade_info_by_name(self, name):
        '''
        根据班级名称查询班级下所有学生
        :param name: 班级名称
        :return: [{'name': name,
                'code': code,
                'gender': gender,
                'grade_id': grade_id}...]
        '''
        data = self.get_or_init(self.key_gradeInfo, {})
        if not data.get(name):
            logging.warning('no cache')

            # self.add_grade_info(name, set(l_stu_id))
            l_stu_id = self.update_grade_info(name)
        else:
            l_stu_id = data['name']

        result = self.get_multi_stu_info(l_stu_id)
        return result

    def read_stu_info_by_name(self, name):
        '''
        根据姓名查询个人信息和班级
        :param name: 姓名
        :return: {'name': name,
                'code': code,
                'gender': gender,
                'grade_id': grade_id，
                'grade_name': grade_name
                }
        '''
        data_map = self.get_or_init(self.key_stuMap, {})
        stu_id = data_map.get(name)

        # 无缓存则更新
        if not stu_id:
            stu = Student.objects.get(name=name)
            info = {
                    'name': stu.name,
                    'code': stu.code,
                    'gender': stu.gender,
                    'grade_id': stu.grade_id,
                    'grade_name': stu.grade_name,
                    'stu_id': stu.id
                }
            self.update_stu_info(**info)
            info['id'] = info.pop('stu_id')  # 统一字段名称
            return info

        # 有stuMap缓存时继续查询详细信息
        stu = self.get_multi_stu_info([stu_id])[0]

        # 获取班级信息
        grade_name = self.get_grad_name_by_id(stu['grade_id'])
        stu['grade_name'] = grade_name
        return stu


class StudentViewSet(viewsets.ModelViewSet):
    '''
    学生API
    '''
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        '''
        增加更新缓存逻辑
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        print("新建时候执行--------------------------")
        resp = super(StudentViewSet, self).create(request, *args, **kwargs)
        # 更新缓存
        map_gender = dict(resp.data.serializer.Meta.model.gender_choices)
        params = {
            'name': resp.data['name'],
            'code': resp.data['code'],
            'gender': map_gender[resp.data['gender']],
            'grade_id': resp.data['grade'],
            'grade_name': resp.data.serializer.validated_data['grade'].name,
            'stu_id': resp.data['id']
        }
        CacheUtils().update_stu_info(**params)

        return resp

    def update(self, request, *args, **kwargs):
        '''
        增加更新缓存逻辑
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        resp = super(StudentViewSet, self).update(request, *args, **kwargs)

        # 更新缓存
        params = {
            'name': resp.data['name'],
            'code': resp.data['code'],
            'gender': resp.data['gender'],
            'grade_id': resp.data['grade_id'],
            'grade_name': resp.data['grade_name'],
            'stu_id': resp.data['id']
        }
        CacheUtils().update_stu_info(**params)
        return resp

    def destroy(self, request, *args, **kwargs):
        return HttpResponseForbidden('禁用')


class GradeViewSet(viewsets.ModelViewSet):
    '''
    班級API
    '''
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def create(self, request, *args, **kwargs):
        '''
        增加更新缓存逻辑
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        print("新建时候执行--------------------------")
        resp = super(GradeViewSet, self).create(request, *args, **kwargs)
        CacheUtils().update_grade_map(resp.data['name'], resp.data['id'])
        return resp

    def update(self, request, *args, **kwargs):
        '''
        增加更新缓存逻辑
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        resp = super(GradeViewSet, self).update(request, *args, **kwargs)
        CacheUtils().update_grade_map(resp.data['name'], resp.data['id'])
        return resp

    def destroy(self, request, *args, **kwargs):
        return HttpResponseForbidden('禁用')