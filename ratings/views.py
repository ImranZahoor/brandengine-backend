from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ratings.models import Ratings
from ratings.serializers import RatingsSerializer
from django.db.models import Q

class RatingsViewSet(viewsets.ModelViewSet):
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_ratings(self, request):
        user = request.user
        user_ratings = self.get_queryset().filter(user=user)
        serializer = self.get_serializer(user_ratings, many=True)
        return Response(serializer.data)

class UserRatingsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RatingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Ratings.objects.filter(user=user)