# Generated by Django 4.1.5 on 2023-01-17 07:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=32)),
                ('code', models.CharField(max_length=8, unique=True, validators=[django.core.validators.RegexValidator('^[0-9 ]*$', 'Only numbers allowed.')])),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女'), (3, '其他')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('my_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserControl.class')),
            ],
        ),
    ]
