from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ThreadModel

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
        return representation

    def create(self, validated_data):
        thread = ThreadModel.objects.create()
        thread.participants.set(validated_data.get('participants'))
        return thread

class MessageSerializers(serializers.Serializer):
    sender = serializers.IntegerField(read_only=True)
    text = serializers.CharField()
    thread = serializers.IntegerField(read_only=True)
    is_read = serializers.BooleanField(default=False)


