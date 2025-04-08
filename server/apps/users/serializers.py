from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, CLASSES


# Расшифровка класса
class ClassOfField(serializers.BaseSerializer):

    def to_representation(self, instance):
        for t in CLASSES:
            if t[0] == instance:
                return t[1]
        return instance


class UserSerializer(serializers.ModelSerializer):
    class_of = ClassOfField()

    class Meta:
        model = User
        fields = ['pk', 'first_name', 'last_name', 'telegram_id',
                  'telegram_username', 'date_joined', 'class_of', 'is_active', 'is_staff', 'token']


# сериализатор пользователя под измененную модель юзера
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # поменяй на нужное поле (например, email)
        self.username_field = "phone"
        return super().validate(attrs)
