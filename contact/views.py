from django.shortcuts import render
from contact.serializers import ContactSerializer
from contact.models import Contact
from rest_framework.response import Response
from rest_framework import status, generics

# Create your views here.

class PostContact(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class=ContactSerializer
    def create(self,request, *args,**kwargs):
        serializer= self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Contact Successfull"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
