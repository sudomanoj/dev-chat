from django.urls import path, include
from rest_framework import routers
from .views import ChatGroupListCreateView

urlpatterns = [
    path('chat_groups/', ChatGroupListCreateView.as_view(), name='chat-group-list-create'),
]
