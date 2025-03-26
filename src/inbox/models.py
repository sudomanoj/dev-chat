from django.db import models
from common.mixins import TimeStampMixin
from uuid import uuid4
from django.contrib.auth import get_user_model
# Create your models here.

class Message(TimeStampMixin):
    """
    Model for storing messages
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    
    sender = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name='sent_messages',
        null=True,
    )
    
    receiver = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name='received_messages',
        null=True,
    )
    
    message = models.TextField()
    
    is_read = models.BooleanField(
        default=False,
    )
    
    def __str__(self):
        return f'{self.sender} -> {self.receiver}'
    
    