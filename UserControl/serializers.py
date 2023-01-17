from UserControl.models import Student, Grade
from rest_framework import serializers


class GradeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'name', 'created_at', 'updated_at')


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    grade = GradeSerializer(read_only=False)

    class Meta:
        model = Student
        fields = ('id', 'name', 'code', 'gender', 'grade', 'created_at', 'updated_at')

    def create(self, validated_data):
        grade_data = validated_data.pop('grade')
        grade, res = grade_name = Grade.objects.get_or_create(name=grade_data['name'])
        validated_data['grade'] = grade

        student = Student.objects.create(**validated_data)
        return student
