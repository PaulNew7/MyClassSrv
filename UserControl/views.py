from django.shortcuts import render
from rest_framework import viewsets

from UserControl.models import Student, Grade
from UserControl.serializers import StudentSerializer, GradeSerializer


class StudentViewSet(viewsets.ModelViewSet):
    '''
    学生API
    '''
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class GradeViewSet(viewsets.ModelViewSet):
    '''
    班級API
    '''
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
