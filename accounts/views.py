from django.shortcuts import render ,redirect
from rest_framework.views import APIView
from .serializers import RegistraionSerializer, UserLoginSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User, Group
from .models import Student,Instructor
# Create your views here.

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class RegistrationView(APIView):
    serializer_class = RegistraionSerializer
    def post(self,request):
        form = self.serializer_class(data=request.data)
        if form.is_valid():
            username = form._validated_data['username']
            password = form._validated_data['password']
            email = form._validated_data['email']
            role = form._validated_data['role']
            user = User.objects.create_user(is_active=False,username=username,email=email,password=password)  
 
            if role in ['Student','Instructor']:
                user.groups.add(Group.objects.get(name=role))   

            token = default_token_generator.make_token(user)
            print(token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print(f"UID: {uid}")
            confirm_link = f"http://127.0.0.1:8000/user/activate/{uid}/{token}"
            email_subject = "Activate you Account "
            email_body = render_to_string('activate_email.html',{'confirm_link':confirm_link})

            email = EmailMultiAlternatives(
                subject=email_subject,
                body='',
                from_email= 'True Learner <noreply@example.com>', 
                to =[user.email]
            )
            email.attach_alternative(email_body, "text/html")
            email.send()
        
            serializer = RegistraionSerializer(user)
            return Response(request.data,status=status.HTTP_200_OK) 
        return Response('error',status=status.HTTP_406_NOT_ACCEPTABLE)

def activate(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except User.DoesNotExist:
        user = None 
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return render(request,'success_activated.html',{}) 

    return render(request,"failed_email.html",{})

class LoginView(APIView):
    def post(self,request):
        serializer = UserLoginSerializers(data=self.request.data)
        if serializer.is_valid():
            user = serializer._validated_data['user']
            if user:
                token , _ = Token.objects.get_or_create(user=user)
                login(request,user)
                return Response({"token":token.key,"user_id":user.id,})
            else:
                return Response({"error":"Invalid Credential"})
        return Response(serializer.errors)
    

class LogoutView(APIView):
    def get(self, request): 
        try:   
            token = Token.objects.get(user=User.objects.get(id=request.user.id))
            token.delete() 
            logout(request) 
            return Response({"message": "Token deleted successfully, user logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid token or token does not exist."}, status=status.HTTP_400_BAD_REQUEST)
