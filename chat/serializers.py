from rest_framework import serializers
from .models import *


class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = "__all__"


class InboxSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(Message, many=True)
    class Meta:
        model = Inbox
        fields = ["messages"]