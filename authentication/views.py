from django.contrib import auth
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import UserSerializer,LoginSerializer,LogoutSerializer


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        data=request.data
        username=data.get('username','')
        password=data.get('password','')
        user=auth.authenticate(username=username,password=password)

        if user:
            refresh=RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            data={'user':serializer.data,'refresh':str(refresh),'access':str(refresh.acces_token)}
            return Response(data,status.HTTP_200_OK)

        return Response({'error':'Invalid Credentials'},status.HTTP_401_UNAUTHORIZED)

class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        serializer=LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error':'Something Went Wrong'})

