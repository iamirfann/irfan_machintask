from django.shortcuts import render

# from authn import serializers
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from django.shortcuts import render, redirect
# from .serializers import RegisterSerializer
from django.contrib.auth import login, logout
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

class RegisterApiView(APIView):
    @csrf_exempt
    def post(self, request):
        req = request.data
        username = req['username']
        email = req['email']
        password = req['password']
        role = req['role']
        get_username = User.objects.filter(username=username).exists()
        if get_username:
            return Response({"error": "username already exists"})
        elif int(role) == 1:
            user = User.objects.create_superuser(username=username, email=email, password=password)
            user.save()
            user.set_password(password)
            user.save()
            return Response({'success': 'admin registered successfully'})
        elif int(role) == 2:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            user.set_password(password)
            user.save()
            return Response({'success': 'user registered successfully'})


class LoginApiView(APIView):
    @csrf_exempt
    def post(self, request):
        req = request.data
        username = req['username']
        password = req['password']
        get_user = User.objects.get(username=username)
        get_user.check_password(password)

        if get_user:
            login(request=request, user=get_user)
            return Response({'success': 'login successfull'})


class LogoutApiView(APIView):
    @csrf_exempt
    def post(self, request):
        logout(request)
        return Response({'success': 'logout successfull'})



