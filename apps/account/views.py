from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serilizers import LoginSerializer, RegisterSerializer, User
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def index(request):
    return render(request, 'account/loginregister.html', {'re': "account"})


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({"token": token.key, "Success": "Login Successfully"})

            return Response({'Message': 'Invalid Username and Password'}, status=401)


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'User created'}, status=201)
        return Response({'Message': serializer.errors}, status=401)


def logout_view(request):
    logout(request)
    return redirect("/")
