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

    
    @action(detail=False, methods=['get'], url_path='brand/(?P<brand_profile_id>\d+)', permission_classes=[IsAuthenticatedOrReadOnly])
    def ratings_by_brand(self, request, brand_profile_id=None):
        try:
            ratings = self.get_queryset().filter(brand_profile=brand_profile_id)
            serializer = self.get_serializer(ratings, many=True)
            return Response(serializer.data)
        except Ratings.DoesNotExist:
            return Response({'detail': 'Ratings not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'], url_path='my_ratings', permission_classes=[IsAuthenticated])
    def rating_by_user(self,request, *args, **kwargs):
        user = self.request.user
        ratings = Ratings.objects.filter(user=user)
        serializer = self.get_serializer(ratings, many=True)
        return Response(serializer.data)

# class UserRatingsViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = RatingsSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Ratings.objects.filter(user=user)
