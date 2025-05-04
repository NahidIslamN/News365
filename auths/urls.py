from django.urls import path
from .views import Register, LoingPage,LogoutView

urlpatterns = [

    path('register/', Register.as_view(), name='registerui' ),
    path('login/', LoingPage.as_view(), name='loginui' ),
    path('logout/', LogoutView.as_view(), name='logoutui')

   
]
