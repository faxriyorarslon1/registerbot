from rest_framework import serializers
from telegram_bot.models import (
        User,
        Student,
        UserStep,
        Course,
        Group,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "user_id", "tg_username")

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("user", "name", "age", "phone", "gender", "group")

    user = serializers.PrimaryKeyRelatedField(read_only=True)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("course_title", "name", "mentor", "time", 
                    "weekdays", "price", "technologies")

    course_title = serializers.PrimaryKeyRelatedField()                    

        