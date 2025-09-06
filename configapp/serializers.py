from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.timezone import now
from .models import User, ToDoList


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"success": False, "detail": "Bunday foydalanuvchi topilmadi."})

        auth_user = authenticate(username=user.username, password=password)
        if auth_user is None:
            raise serializers.ValidationError({"success": False, "detail": "Username yoki parol noto‘g‘ri."})

        attrs["user"] = auth_user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "is_admin", "is_user", "is_active"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class ToDoListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ToDoList
        fields = ["id", "title", "bajarilgan", "done_time", "user"]

    def update(self, instance, validated_data):
        bajarilgan = validated_data.get("bajarilgan", instance.bajarilgan)
        if bajarilgan and not instance.done_time:
            instance.done_time = now()
        return super().update(instance, validated_data)

class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)