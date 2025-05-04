from rest_framework import serializers 
from users.models import CustomUser
from apis.models import News365, Category
from rest_framework.authtoken.models import Token

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','username','email','password','profile_images']

    def validate(self, data):
        if data['email'] is None:
            raise serializers.ValidationError({
                "error":"email is required"
            })

        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username'],
            email = validated_data['email']
        )
        
        # Handle profile image if provided
        if 'profile_images' in validated_data and validated_data['profile_images']:
            user.profile_images = validated_data['profile_images']
            
        user.set_password(validated_data['password'])
        user.save()

        token = Token.objects.create(user = user)
        token.save()

        return validated_data
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


#######

#News Related Apis

class NewsSerializerPublic(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%B %d, %Y, %I:%M %p")    
    class Meta:
        model = News365
        fields = "__all__"
        
class NewsSerializerPrivate(serializers.ModelSerializer):
    class Meta:
        model = News365
        fields = "__all__"

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
    

        
