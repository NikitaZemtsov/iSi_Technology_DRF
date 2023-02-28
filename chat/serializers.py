from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ThreadModel, MessageModel

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk']

class ThreadSerializers(serializers.Serializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    def validate_participants(self, value):
        if not len(value) == 2:
            raise serializers.ValidationError("Participants should consist only two users pk.")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['pk'] = instance.pk
        representation['message'] = instance.messagemodel_set.filter(is_read=False).order_by('-created')
        return representation

    def create(self, validated_data):
        thread = ThreadModel.objects.create()
        thread.participants.set(validated_data.get('participants'))
        return thread

    def check_thread_exist(self):
        users = self.validated_data.get('participants')
        thread = list(set(users[0].threads.all()) & set(users[1].threads.all()))
        return thread[0] if len(thread) == 1 else False


class MessageSerializers(serializers.Serializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    text = serializers.CharField()
    thread = serializers.PrimaryKeyRelatedField(queryset=ThreadModel.objects.all())
    is_read = serializers.BooleanField(default=False)
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        msg = MessageModel.objects.create(**validated_data)
        return msg

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['pk'] = instance.pk
        representation['created'] = instance.created
        return representation