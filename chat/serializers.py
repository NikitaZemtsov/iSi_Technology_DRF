from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ThreadModel

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']

class ThreadSerializers(serializers.Serializer):
    participants = UserSerializer(many=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        thread = ThreadModel.objects.create()
        thread.participants.set(validated_data.get('participants'))
        return thread

class MessageSerializers(serializers.Serializer):
    sender = serializers.IntegerField(read_only=True)
    text = serializers.CharField()
    thread = serializers.IntegerField(read_only=True)
    is_read = serializers.BooleanField(default=False)


