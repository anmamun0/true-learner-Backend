from rest_framework import serializers
from django.contrib.auth.models import User, Group

from .constraint import ROLE_CHOICES
from django.contrib.auth import authenticate


class RegistraionSerializer(serializers.ModelSerializer): 
    role = serializers.ChoiceField(choices=ROLE_CHOICES,required=True)
    phone = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    class Meta:
        model = User 
        fields = ['role','username','first_name','last_name','email','phone','address','password']

    def validate_username(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({'error_username':'username is already exist.',})
        return value
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({'error_email':'email is already exist Account, Please login!'})
        return value 
    

class UserLoginSerializers(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True,required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        user = authenticate(username=username,password=password)
        if not user:
            raise serializers.ValidationError('Inalid User')
        if not user.is_active:
            raise serializers.ValidationError('User account is inactive!')
        
        attrs['user'] = user
        return attrs
    
