from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from followertrack.models import FollowerTrack
from followertrack.serializers import FollowerTrackSerializer


class FollowerTrackViewSet(viewsets.ModelViewSet):
    queryset = FollowerTrack.objects.all()
    serializer_class = FollowerTrackSerializer
    permission_classes = [IsAuthenticated]
