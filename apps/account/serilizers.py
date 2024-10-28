from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if not data.get('email') and data.get('password'):
            raise serializers.ValidationError("Both password and email are required")
        return data


