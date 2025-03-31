from django.db import models
from .user_manager import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from common.mixins import TimeStampMixin
from uuid import uuid4


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    
    email = models.EmailField(
        max_length=255,
        unique=True,
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )
    
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        error_messages={
            'unique': "A user with that phone number already exists.",
        },
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
        verbose_name='active',
    )
    
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.',
        verbose_name='staff status',
    )
    
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date joined',
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']
    
    def __str__(self):
        return self.email or self.phone_number
    
    
    
class ChatGroup(TimeStampMixin):
    """
    Model representing a chat group.
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    
    name = models.CharField(
        max_length=255,
        unique=True,
        error_messages={
            'unique': "A group with that name already exists.",
        },
    )
    
    description = models.TextField(
        blank=True,
        null=True,
    )
    
    
    def __str__(self):
        return self.name
    
    
class UserGroup(TimeStampMixin):
    """
    Model representing the relationship between a user and a chat group.
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_groups',
    )
    
    group = models.ForeignKey(
        ChatGroup,
        on_delete=models.CASCADE,
        related_name='group_users',
    )
    
    is_owner = models.BooleanField(
        default=False,
        help_text='Designates whether the user is the owner of the group.',
    )
    
    is_admin = models.BooleanField(
        default=False,
        help_text='Designates whether the user is an admin of the group.',
    )
    
    def __str__(self):
        return f"{self.user.email} - {self.group.name}"
    
    class Meta:
        unique_together = ('user', 'group')
        verbose_name = 'User Group'
        verbose_name_plural = 'User Groups'