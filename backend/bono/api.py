# bono/api.py
from rest_framework import viewsets
from .models import Bonos, GeneratedBono
from .serializers import BonoSerializer, GeneratedBonoSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Override to exclude users marked as 'is_deleted'.
        Only non-deleted users will be retrieved.
        """
        return User.objects.filter(is_deleted=False)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_profile(self, request):
        """
        Custom action to retrieve the profile of the currently authenticated user.
        """
        try:
            user = request.user
            user_data = User.objects.get(id=user.id)

            # Serialize user profile data
            profile_data = self.get_serializer(user_data).data
            return Response(profile_data)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        """
        Custom create method to automatically set `added_by` field to the requesting user.
        """
        user = serializer.save(added_by=self.request.user)
        return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        """
        Custom update method to log the user who performed the update.
        Sets both `updated_by` and `status_changed_by` to the requesting user.
        """
        serializer.save(updated_by=self.request.user, status_changed_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method to mark a user as deleted rather than removing the record.
        Sets `is_deleted=True`, `deleted_by` to the requesting user, and saves.
        """
        instance = self.get_object()
        instance.is_deleted = True  # Mark as deleted
        instance.deleted_by = request.user
        instance.save()

        # Optionally, you could return a custom message or data
        return Response({"message": "User marked as deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class BonoViewSet(viewsets.ModelViewSet):
    queryset = Bonos.objects.all()
    serializer_class = BonoSerializer

# GeneratedBono ViewSet
class GeneratedBonoViewSet(viewsets.ModelViewSet):
    queryset = GeneratedBono.objects.all()
    serializer_class = GeneratedBonoSerializer