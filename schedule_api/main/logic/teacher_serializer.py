from rest_framework import serializers
from schedule_api.main.models.teacher import Teacher


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'middle_name', 'last_name', 'teaching_subject', 'active',)
