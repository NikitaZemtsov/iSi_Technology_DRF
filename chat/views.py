from django.shortcuts import render
from rest_framework import generics
from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ThreadModel, MessageModel
from django.contrib.auth.models import User
from .serializers import ThreadSerializers, MessageSerializers


class ThreadApiView(APIView):

    def get(self, request, thread_id):
        thread = ThreadModel.objects.filter(pk=thread_id).first()
        MessageSerializers(data=thread.messagemodel_set.all().order_by('-created'), many=True)
        return Response({'message': MessageSerializers(data=thread.messagemodel_set.all(), many=True)})

    def post(self, request, thread_id):
        thread = ThreadModel.objects.filter(pk=thread_id).first()
        serializers = MessageSerializers(data=request.data, many=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({'message': serializers.data})


class UserThread(APIView):

    def get(self, request):
        user_id = request.GET.get('user_id')
        user = User.objects.filter(pk=user_id).first() if user_id else self.request.user
        threads = user.threads.all()
        return Response({'thread': ThreadSerializers(threads, many=True).data})

    def post(self, request):
        serializers = ThreadSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        thread = serializers.check_thread_exist()
        if thread:
            return Response({'thread': ThreadSerializers(thread).data})
        serializers.save()
        return Response({'thread': serializers.data})


class UserMsg(APIView):
    def get(self, request):
        user_id = request.GET.get("user_id")
        new = not bool(request.GET.get("new", False))
        user = User.objects.filter(pk=user_id) if user_id else self.request.user
        msg = MessageModel.objects.filter(thread_in=user.thread.all(), is_read=new)
        return Response({'msg': MessageSerializers(msg, many=True).data})

    def post(self, request):
        pass
