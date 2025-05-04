from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
import requests
from django.urls import reverse
from django.http.response import HttpResponse

from auths.froms import NewsCreateForm

from django.contrib import messages


# Create your views here.






class MyNews(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        token = Token.objects.get(user = user)
        api_url = request.build_absolute_uri(reverse('mynews'))

        headers = {
            "Authorization": f"Token {token}"
        }

        response = requests.get(api_url, headers=headers)
        jsondata = None
        
        if response.status_code == 200:
            jsondata = response.json()
        
        newsforms = NewsCreateForm()

      
        cp = {
            "mynews":jsondata,
            "forms":newsforms,
        }

        return render(request, 'mynews.html', context=cp)
    
    @method_decorator(login_required)
    def post(self, request):

        data = request.POST.copy()

        api_url = request.build_absolute_uri(reverse('mynews'))
        
        token = Token.objects.get(user = request.user)

        files = {

        }  

        headers = {
            'Authorization': f'Token {token.key}',  # Make sure to use .key
        }



        for field_name in ['image1', 'image2', 'image3', 'adverticement']:
            uploaded_file = request.FILES.get(field_name)
            if uploaded_file:
                files[field_name] = (
                    uploaded_file.name, uploaded_file, uploaded_file.content_type
                )

                headers = {
                    'Authorization': f'Token {token}',
                }
            else:
                data.pop(field_name, None)

        

        response = requests.post(
            api_url,
            data=data,
            files=files,
            headers=headers
        )
       
        if response.status_code == 201:
            messages.info(request,"Successfully add the news!")
            return redirect('/users/mynews/')
            

        return HttpResponse('401 BAD Request')
    


class UserNewsDetails(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        user = request.user
        token = Token.objects.get(user = user)
        api_url = request.build_absolute_uri(reverse('newsdetailsprivate', args=[pk]))

        headers = {
            "Authorization": f"Token {token}"
        }

        response = requests.get(api_url, headers=headers)
        jsondata = None
        forms = None
        
        
        if response.status_code == 200:
            jsondata = response.json()
            forms = NewsCreateForm(data=jsondata)

     
        cp = {
            "mynews":jsondata,
            'forms':forms,
           
            
        }

        return render(request, 'usernewsdetails.html', context=cp)
    

    @method_decorator(login_required)
    def post(self, request, pk):
        methods = request.POST.get('_method', '').upper()

        if methods == 'DELETE':
            
            api_url = request.build_absolute_uri(reverse('newsdetailsprivate', args=[pk]))
            
            token = Token.objects.get(user = request.user)
            headers = {
                'Authorization': f'Token {token.key}',  # Make sure to use .key
            }
            response = requests.delete(
                api_url,
                headers=headers
            )
            if response.status_code == 200:
                messages.info(request,"Delete New Successfull!")
                return redirect(f'/users/mynews/')






        
        data = request.POST.copy()
        api_url = request.build_absolute_uri(reverse('newsdetailsprivate', args=[pk]))
        token = Token.objects.get(user = request.user)

        files = {

        }  

        headers = {
            'Authorization': f'Token {token.key}',  # Make sure to use .key
        }



        for field_name in ['image1', 'image2', 'image3', 'adverticement']:
            uploaded_file = request.FILES.get(field_name)
            if uploaded_file:
                files[field_name] = (
                    uploaded_file.name, uploaded_file, uploaded_file.content_type
                )

                headers = {
                    'Authorization': f'Token {token}',
                }
            else:
                data.pop(field_name, None)

        

        response = requests.put(
            api_url,
            data=data,
            files=files,
            headers=headers
        )
       
        if response.status_code == 200:
            messages.info(request,"Successfully Update the news!")
            return redirect(f'/users/mynews/{pk}/')
            

        # 
        return HttpResponse('401 BAD Request')
        
        