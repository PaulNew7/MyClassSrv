from UserControl.models import Student, Grade
from rest_framework import serializers


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'name', 'created_at', 'updated_at')


class StudentSerializer(serializers.ModelSerializer):
    # grade = GradeSerializer(read_only=False)
    grade = serializers.PrimaryKeyRelatedField(label='班级',
                                               queryset=Grade.objects.all())

    class Meta:
        model = Student
        fields = ('id', 'name', 'code', 'gender', 'grade', 'created_at', 'updated_at')

    def create(self, validated_data):
        student = Student.objects.create(**validated_data)
        return student

    # def update(self, instance, validated_data):
    #     student = Student.objects.filter(id=instance.id).update(**validated_data)
    #     return student
