from rest_framework import serializers
from ratings.models import Ratings
from drf_extra_fields.fields import Base64ImageField


class RatingsSerializer(serializers.ModelSerializer):
    proof_of_order = Base64ImageField(required=False)

    class Meta:
        model = Ratings
        fields = ("id","description", "proof_of_order", "brand_profile", "rating", "user")
        extra_kwargs = {
            "proof_of_order": {"required": True},
            "brand_profile": {"required": True},
            "rating": {"required": True},
            "id": {"read_only": True},
        }
