from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView, LetestNews, NewsCURD,NewsDetailsPublic, NewsDetailsPrivate, NewsCategoryPublic, NewsCategoryPrivate,Allapi

urlpatterns = [
    path('', Allapi.as_view(), name="apis"),

    path('register/', RegisterView.as_view(), name='register' ),
    path('login/', LoginView.as_view(), name='loginapi' ),
    path('logout/', LogoutView.as_view(), name="logoutapi" ),
    path('latest-news/', LetestNews.as_view(), name='latestnews'),
    path('my-news/', NewsCURD.as_view(), name='mynews'),
    path('news-details-public/<pk>/', NewsDetailsPublic.as_view(), name="newsdetailspublic"),
    path('news-details-private/<pk>/', NewsDetailsPrivate.as_view(), name="newsdetailsprivate"),
    path("news-categories/", NewsCategoryPublic.as_view(), name="categoris"),
    path("news-categories/<pk>/", NewsCategoryPrivate.as_view(), name="categorisprivate")
    
   
]
