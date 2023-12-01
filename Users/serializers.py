from rest_framework import serializers
from .models import CustomUser, TrainerProfile


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name',
                  'is_superuser', 'is_trainer', 'is_member']


class TrainerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainerProfile
        fields = ['trainer_id', 'user']
