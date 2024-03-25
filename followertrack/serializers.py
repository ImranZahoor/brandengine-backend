from rest_framework import serializers
from followertrack.models import FollowerTrack


class FollowerTrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowerTrack
        fields = ("brand_profile", "insta_count", "fb_count")
