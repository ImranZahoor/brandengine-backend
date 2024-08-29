from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from subscription.serializers import SubcriberSerailizer
from .models import Subscriber
from rest_framework import generics

# Create your views here.

class SubscribeView(generics.CreateAPIView):
    queryset=Subscriber.objects.all()
    serializer_class=SubcriberSerailizer
    
    def create(self,request, *args,**kwargs):
        serializer= self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Subscription Successfull"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)