from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from brandprofile.models import BrandProfile, Category


class BrandProfileSerializer(serializers.ModelSerializer):
    logo = Base64ImageField(required=False)

    class Meta:
        model = BrandProfile
        fields = (
            "id",
            "name",
            "search_tags",
            "website",
            "description",
            "logo",
            "insta",
            "facebook",
            "country",
            "city",
            "address",
            "phone",
            "email",
            "owner",
            "category",
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("id", "name")
