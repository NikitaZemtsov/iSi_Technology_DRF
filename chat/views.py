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
        ''' get list of message
        :parameter
            ?filter = new - only new message
            ?offset=1000 - first 1000
                    -1000 - last 1000
            ?limit =
        '''
        return Response({'title':'lskjdf'})

    def post(self, request):
        return Response({})


class UserThread(APIView):

    def get(self, request):
        user_id = request.GET.get('user_id')
        user = User.objects.filter(pk=user_id).first() if user_id else self.request.user
        thread = user.threadmodel_set.all().values()
        return Response({'thread': ThreadSerializers(thread, many=True).data})

    def post(self, request):
        serializers = ThreadSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        print(serializers.data)
        return Response(serializers.data)


class UserMsg(APIView):
    def get(self, request):
        user_id = request.GET.get("user_id")
        new = not bool(request.GET.get("new", False))
        user = User.objects.filter(pk=user_id) if user_id else self.request.user
        msg = MessageModel.objects.filter(thread_in=user.thread.all(), is_read=new)
        return Response({'msg': MessageSerializers(msg, many=True).data})

    def post(self, request):
        pass
