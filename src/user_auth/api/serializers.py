from rest_framework import serializers
from ..models import ChatGroup


class ChatGroupSerializer(serializers.ModelSerializer):
    """
    Serializer for the ChatGroup model.
    """
    user_email = serializers.SerializerMethodField()
    class Meta:
        model = ChatGroup
        fields = ('uuid', 'name', 'description', 'user_email')
        read_only_fields = ('uuid',)
        
    def get_user_email(self, obj):
        """
        Get the full name of the user.
        """
        return [f"{group_users.user.email}" for group_users in obj.group_users.all()]