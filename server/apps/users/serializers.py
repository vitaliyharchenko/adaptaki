from rest_framework import serializers
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
                  'telegram_username', 'date_joined', 'class_of']
