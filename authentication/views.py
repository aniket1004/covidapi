from django.shortcuts import render
from rest_framework import generics,status,views,permissions
from .serializer import RegisterSerializer,EmailVerificationSerializer,LoginSerializer,LogoutSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import  User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import  reverse
import jwt
from django.conf import settings
from drf_yasg.utils import  swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRender

import ast
# Create your views here.
class RegistrationView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRender,)
    
    def post (self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception =True)
        serializer.save()
        
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])        
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request)
        relative_link = reverse('email-verify')
        absurl = 'http://'+current_site.domain+relative_link+"?token="+str(token)
        email_body = 'Hi '+user.username+' User link to verify email \n'+absurl
        data = {'email_body': email_body,'email_subject':'Verify your email','to': user.email}
        Util.send_email(data)
        return Response(user_data,status=status.HTTP_201_CREATED)
    
class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)
    renderer_classes = (UserRender,)
    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token = request.GET.get('token')
        print('token',token)
        print('key',settings.SECRET_KEY)
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
            print('payload',payload)
            user = User.objects.get(id = payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email':'Successfully activated'},status=status.HTTP_200_OK)
         
        except jwt.ExpiredSignatureError as  identifier:
            return Response({'error' : 'Activation expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as  identifier:
            return Response({'error' : 'Invalid token'},status=status.HTTP_400_BAD_REQUEST)
        
      
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    renderer_classes = (UserRender,)
    def post(self,request):
        # data = request.data
        # d = data.get('data')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception = True)        
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
      