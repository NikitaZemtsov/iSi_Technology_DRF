from django.db import models
from django.contrib.auth.models import User


class ThreadModel(models.Model):
    participants = models.ManyToManyField(User, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Thread:{self.pk}'


class MessageModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    thread = models.ForeignKey(ThreadModel, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message: {self.pk} in thread: {self.thread}'
