
from rest_framework import serializers
from django.contrib import  auth
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken ,TokenError
from rest_framework.exceptions import AuthenticationFailed
from .renderers import UserRender

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68,min_length=6,write_only=True)
    
    class Meta:
        model = User
        fields = ['email','username','password'] 
        
    def validate(self,attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')
        
        if not username.isalnum():
            raise serializers.ValidationError('The username should only contains alphanumeric')
        return attrs
    
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
        
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    
    class Meta:
        model = User
        fields = ['token']
        
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,min_length=3)
    password = serializers.CharField(max_length=68,min_length=6,write_only=True)
    username = serializers.CharField(max_length=255,min_length=3,read_only=True)
    tokens = serializers.SerializerMethodField()
    
    def get_tokens(self,obj):
        user = User.objects.get(email=obj['email'])
        return {
            'access' : user.tokens()['access'],
            'refresh' : user.tokens()['refresh']
        }
    class Meta:
        model = User
        fields = ['email','password','username','tokens']
        
    def validate(self,attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user = auth.authenticate(email=email,password=password)
        
        if not user:
            raise AuthenticationFailed('Invalid credentials ,try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled ,contact admin')
        if not user.is_verified:
            AuthenticationFailed('Email is not verified')
            
        return {
            'email' : user.email,
            'username' : user.username,
            'tokens': user.tokens
        } 
        
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    default_error_messages = {
        'bad_token': 'Token is expired or invalid'
    }
    def validate(self,attrs):
        self.token = attrs['refresh']
        
        return attrs
    
    def save(self, **kargs):
        try:
            RefreshToken(self.token).blacklist()
            
        except TokenError:
            self.fail('bad_token')
            