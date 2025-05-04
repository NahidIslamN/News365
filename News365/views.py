from django.shortcuts import render

from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import requests
from django.http.response import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode

class Homepapge(View):

    def get(self, request):

        search_quiry = request.GET.get('search')
        
        base_url = request.build_absolute_uri(reverse('latestnews'))

        if search_quiry:
            query_string = urlencode({'search': search_quiry})
            api_url = f"{base_url}?{query_string}"
        else:
            api_url = base_url


        
        


        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                latest_news = response.json()  # Assuming the API returns JSON
                
            else:
                latest_news = []
        except requests.exceptions.RequestException as e:
            return HttpResponse ('news not found')
            

        return render(request, 'index.html', {'latest_news': latest_news})
    




class NewsDetail(View):
    def get(self, request, pk):  

        api_url = request.build_absolute_uri(reverse('newsdetailspublic', kwargs={'pk': pk}))
       
        response = requests.get(api_url)

        cp = {
            "news" : response.json()
        }


        return render(request, 'newsdetails.html', context=cp)