from rest_framework import serializers
from ratings.models import Ratings
from users.serializers import UserSerializer

class RatingsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Ratings
        fields = ("description", "proof_of_order", "brand_profile", "rating", "user")
        extra_kwargs = {
            "proof_of_order": {"required": True},
            "brand_profile": {"required": True},
            "rating": {"required": True},
        }
