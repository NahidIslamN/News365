from django.urls import path, include
from .views import MyNews,UserNewsDetails

urlpatterns = [

    path('mynews/', MyNews.as_view(), name='usernews' ),
    path('mynews/<pk>/', UserNewsDetails.as_view(), name='usernews' ),

 

   
]
