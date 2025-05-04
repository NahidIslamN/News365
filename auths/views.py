
from django.shortcuts import render, redirect
from django.views import View
from .froms import RegisterFrom, LoginForm
from rest_framework.authtoken.models import Token
from django.contrib import messages
import requests

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse

# Create your views here.

class LoingPage(View):
    def get(self, request):

        login = LoginForm()

        cp = {
            'login':login
        }

        return render(request, 'loginpage.html', context=cp)
    def post(self, request):
        api_url =api_url = request.build_absolute_uri(reverse('loginapi'))
        data = request.POST


        user = authenticate(username = data['username'], password = data['password'])
        if user:
            login(request,user) 
            return redirect('/')
        else:
            messages.info(request,"login fail!")
            return redirect('/auth/login/')
           


class Register(View):
    @method_decorator(login_required)
    def get(self, request):        

        cp = {
            'register':RegisterFrom,
            
        }
        return render(request,'register.html', context=cp)
    
    @method_decorator(login_required)
    def post(self, request):
        api_url =api_url = request.build_absolute_uri(reverse('register'))# how to use here url with url name?
        token = Token.objects.get(user = request.user)

        data = request.POST


        headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"  # Ensure you send data as JSON
        }

        response = requests.post(api_url, json=data, headers=headers)

        if response.status_code == 201:
            messages.info(request,"Registrations Successfull!")
        else:
            messages.info(request,"Registrations Dineyed!")

        return redirect('/auth/register/')
    


class LogoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        api_url = request.build_absolute_uri(reverse('logoutapi'))
        
        token = Token.objects.get(user = request.user)
        headers = {
            "Authorization": f"Token {token}"
        }
        response = requests.get(api_url, headers=headers)
        

        if response.status_code == 200:
            logout(request)
            return redirect('/')
        else:
            return redirect('/')


        


