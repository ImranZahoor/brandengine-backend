from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ratings.models import Ratings
from ratings.serializers import RatingsSerializer


class RatingsViewSet(viewsets.ModelViewSet):
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Optionally, you can filter the queryset based on the logged-in user
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(user=user)
        return queryset
