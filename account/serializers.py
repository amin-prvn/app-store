from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import User


class RegisterSerializer(serializers.Serializer):
    
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": ["Password fields didn't match."]})
        return attrs

    def create(self, validated_data):
        user : User = User(
            username=validated_data['username'].lower(), 
            email = validated_data['email'],
            )
        user.set_password(validated_data['password'])
        user.last_login = timezone.now()
        user.save()
        return user
    
    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        user_serializer = UserSerializer(instance)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'profile': user_serializer.data
        }


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)

        # Extra responses here
        user_serializer = UserSerializer(self.user)
        data['profile'] = user_serializer.data
        return data


class UserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = User
        fields = ['username', 'email', 'credit']
        read_only_fields = fields