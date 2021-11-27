from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.Serializer):
    username=serializers.CharField(min_length=2,max_length=100)
    firstname=serializers.CharField(min_length=2,max_length=100)
    lastname=serializers.CharField(min_length=2,max_length=100)
    email=serializers.EmailField(min_length=6,max_length=255)
    password=serializers.CharField(min_length=4,max_length=100,write_only=True)

    class Meta:
        model=User
        field=['username','firstname','lastname','email','password']

    def validate(self, data):
        username=data.username
        email=data.email
        if User.objects.filter(username=username).exits():
            raise serializers.ValidationError({'username': ('Username is already in use')})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': ('Email is already in use')})
        return super().validate(data)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(min_length=2,max_length=100)
    password=serializers.CharField(min_length=4,max_length=100,write_only=True)

    class Meta:
        model=User
        fields=['username','password']

class LogoutSerializer(serializers.Serializer):
    token=serializers.CharField()

    def validate(self, data):
        self.token=data['token']
        return data

    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            return 'Token is Expired or Invalid'

