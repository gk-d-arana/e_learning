from django.db import models

from users.models import Instructor


class Message(models.Model):
    message = models.TextField(blank=True)
    message_from = models.ForeignKey(Instructor, on_delete=models.DO_NOTHING, related_name="message_from")
    message_to = models.ForeignKey(Instructor, on_delete=models.DO_NOTHING, related_name="message_to")
    message_sent = models.DateTimeField(auto_now_add=True)
    message_delivered = models.DateTimeField(auto_now_add=True)
    message_seen = models.DateTimeField(auto_now_add=True)
    message_is_sent = models.BooleanField(default=True)
    message_is_delivered = models.BooleanField(default=False)
    message_is_seen = models.BooleanField(default=False)


class Inbox(models.Model):
    inbox_owner = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="inbox_owner")
    messages = models.ManyToManyField(Message, blank=True)


class ChatRoom(models.Model):
    chat_room_participants = models.ManyToManyField(Instructor, blank=True)
    messages = models.ManyToManyField(Message, blank=True)