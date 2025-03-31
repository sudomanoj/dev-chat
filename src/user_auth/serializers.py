from rest_framework import serializers
from .models import ChatGroup


class ChatGroupSerializer(serializers.ModelSerializer):
    """
    Serializer for the ChatGroup model.
    """
    class Meta:
        model = ChatGroup
        fields = ('uuid', 'name', 'description')
        read_only_fields = ('uuid',)