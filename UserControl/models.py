from django.db import models

# Create your models here.
from django.utils import timezone
from django.core.validators import RegexValidator

# alpha_spaces = RegexValidator(r'^[a-zA-Z]*$', 'Only letters and spaces allowed.')
num_only = RegexValidator(r'^[0-9 ]*$', 'Only numbers allowed.')


class Student(models.Model):
    gender_choices = (
        (1, '男'), (2, '女'), (3, '其他')
    )
    name = models.CharField(max_length=32, blank=False, null=False, db_index=True)
    code = models.CharField(max_length=8, blank=False, null=False, validators=[num_only], unique=True)
    gender = models.SmallIntegerField(blank=False, null=False, choices=gender_choices)
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Grade(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
