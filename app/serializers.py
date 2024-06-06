from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Friend

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'].lower(),  # Set username as email for consistency
            email=validated_data['email'].lower(),  # Store email in lowercase
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__' 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email']
