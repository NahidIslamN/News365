from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, NewsSerializerPublic, NewsSerializerPrivate,NewsCategorySerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token
from apis.models import News365, Category
from rest_framework.parsers import MultiPartParser, FormParser


from django.views import View
from django.shortcuts import render
from django.urls import reverse



class Allapi(View):
    def get(self, request):
        allapi = {
            "register":request.build_absolute_uri(reverse('register')),
            "mynews":request.build_absolute_uri(reverse('mynews')),
            "latestnews":request.build_absolute_uri(reverse('latestnews')),
            "login":request.build_absolute_uri(reverse('logoutapi')),
            "logout":request.build_absolute_uri(reverse('loginapi')),
            "news-details-public":request.build_absolute_uri(reverse('newsdetailspublic',args=[1])),
            "news-details-private":request.build_absolute_uri(reverse('newsdetailsprivate',args=[1])),
            "news-details-private":request.build_absolute_uri(reverse('categoris')),
            "news-categories": request.build_absolute_uri(reverse('newsdetailsprivate',args=[1])),
            "news-categories-Private": request.build_absolute_uri(reverse('categorisprivate',args=[1])),

            
            
            }
        cp = {
            "apis":allapi
        }
        return render(request,'apis.html', context=cp)



# Create your views here.

class RegisterView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.is_superuser:
            data = request.data
            serializer = RegisterSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        else:
            return Response({
                "status":"not okey",
                "error":"only admin can create an user!"
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
    
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username = username, password = password)
            token = Token.objects.get(user.user)
         
            if user:
                login(request, user)
                
                
                return Response({
                    "status":"ok",
                    "message":"login success",
                    
        
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status":"not ok",
                    "details":"username or password is not valid",
                    
                },
                status = status.HTTP_400_BAD_REQUEST
                )
            
        
        return Response({
            "status":"not ok",
            "details":"username or password is not valid"
        },
        status = status.HTTP_400_BAD_REQUEST
        )
    



class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(request.user)
        
        Token.objects.get(user=request.user).delete()

        # Create a new token
        new_token = Token.objects.create(user=request.user)
        new_token.save()

        logout(request)
        

        
        return Response(
            {
            "status":"ok"
            },
        status=status.HTTP_200_OK)
        
       




   


# news related apis




class LetestNews(APIView):
    def get(self, request):
        search_query = request.GET.get('search', '').strip()
        if search_query:
            latest_news = News365.objects.filter(category__category=search_query).order_by('-created_at')
        else:
            latest_news = News365.objects.filter().order_by('-created_at')        
        

        serializer = NewsSerializerPublic(latest_news, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NewsCURD(APIView):
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        my_news = News365.objects.filter(creator = user).order_by('-created_at')
        serializerss = NewsSerializerPublic(my_news, many=True)
        return Response(serializerss.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        user = request.user
        data = request.data
        
        data = data.dict()
        
        data['creator'] = request.user.id
      
        serializer = NewsSerializerPrivate(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NewsDetailsPublic(APIView):
    def get(self, request, pk):
        try:
            news = News365.objects.get(id = pk)
        except News365.DoesNotExist:
            return Response({
                "status":"Bad Request",
                "details":"News Not found!"
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        serializer = NewsSerializerPublic(news)
        return Response (serializer.data, status=status.HTTP_200_OK)
    


class NewsDetailsPrivate(APIView):
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            news = News365.objects.get(id = pk)
            if news.creator == request.user or request.user.is_superuser:
                pass
            else:
                return Response(
                    {
                        "status":"update fail!",
                        'details':"it is not created by you!"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except News365.DoesNotExist:
            return Response({
                "status":"Bad Request",
                "details":"News Not found!"
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        serializer = NewsSerializerPublic(news)
        return Response (serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        data = request.data.copy()
        data["creator"] = request.user.id
        print(data)
        try:
            news = News365.objects.get(id = pk)
            if news.creator == request.user or request.user.is_superuser:
                pass
            else:
                return Response(
                    {
                        "status":"update fail!",
                        'details':"it is not created by you!"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except News365.DoesNotExist:
            return Response({
                "status":"Bad Request",
                "details":"News Not found!"
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        serializer = NewsSerializerPrivate(instance=news, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_200_OK)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            news = News365.objects.get(id = pk)
            if news.creator == request.user or request.user.is_superuser:
                news.delete()
                return Response({
                    "status":"Delete Successfull!",
                    "details":"you successfully deleted the news!"
                })
            else:
                return Response(
                    {
                        "status":"delete fail!",
                        'details':"it is not created by you!"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except News365.DoesNotExist:
            return Response({
                "status":"Bad Request",
                "details":"News Not found!"
            },
            status=status.HTTP_400_BAD_REQUEST
            )
   
      
            
    
class NewsCategoryPublic(APIView):
    def get(self, request):
        caterory = Category.objects.filter(status=True)
        serializers = NewsCategorySerializer(caterory, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


    
class NewsCategoryPrivate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            catergory_object = Category.objects.get(id=pk)
            if request.user.is_superuser:
                pass
            else:
                return Response({
                "status":"not valid user!",
                "details":"only admin can call the api!"
            },
            status = status.HTTP_400_BAD_REQUEST
            )
                

        except Category.DoesNotExist:
            return Response({
                "status":"not found!"
            },
            status = status.HTTP_400_BAD_REQUEST
            )
        
        serializer = NewsCategorySerializer(catergory_object)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, pk):
        data = request.data
        if request.user.is_superuser:
            serializer = NewsCategorySerializer(data = data)
            if serializer.is_valid():
                serializer.save()        
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "status":"not ok",
            "details":"only admin can post here"
        })
    
    def put(self, request, pk):
        try:
            catergory_object = Category.objects.get(id=pk)
            if request.user.is_superuser:
                pass
            else:
                return Response({
                "status":"not valid user!",
                "details":"only admin can call the api!"
            },
            status = status.HTTP_400_BAD_REQUEST
            )
                

        except Category.DoesNotExist:
            return Response({
                "status":"not found!"
            },
            status = status.HTTP_400_BAD_REQUEST
            )
        
        serializer = NewsCategorySerializer(instance=catergory_object, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk):
        try:
            catergory_object = Category.objects.get(id=pk)
            if request.user.is_superuser:
                catergory_object.delete()
                return Response(
                    {
                        "status": 'ok',
                        "details":'delete successfully',
                    }
                )
            else:
                return Response({
                "status":"not valid user!",
                "details":"only admin can call the api!"
            },
            status = status.HTTP_400_BAD_REQUEST
            )
                

        except Category.DoesNotExist:
            return Response({
                "status":"not found!"
            },
            status = status.HTTP_400_BAD_REQUEST
            )
        

    
    
        
