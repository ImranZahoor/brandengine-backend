from rest_framework import serializers
from ratings.models import Ratings


class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ("description", "proof_of_order", "brand_profile", "rating")
        extra_kwargs = {
            "proof_of_order": {"required": True},
            "brand_profile": {"required": True},
            "rating": {"required": True},
        }
