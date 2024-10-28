from rest_framework import serializers
from django.contrib.auth import get_user_model
from .validators import CustomPasswordValidator
User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if not data.get('email') and data.get('password'):
            raise serializers.ValidationError("Both password and email are required")
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Passwords must match")

        CustomPasswordValidator().validate(data.get('password'))

        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError("Email already exists")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        user = User.objects.create_user(password=password, email=validated_data.get('email'))
        return user

