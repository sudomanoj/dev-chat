from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import ChatGroup
from .serializers import ChatGroupSerializer


class ChatGroupListCreateView(generics.ListCreateAPIView):
    """
    View to list and create chat groups.
    """
    queryset = ChatGroup.objects.all()
    serializer_class = ChatGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get the list of chat groups.
        """
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create a new chat group.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

