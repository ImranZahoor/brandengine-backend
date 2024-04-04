from rest_framework import serializers

from brandprofile.models import BrandProfile, Category
from draft_profile.models import DraftProfile


class DraftProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = DraftProfile
        fields = (
            "id",
            "brand_name",
            "title",
            "query",
            "url",
            "description",
            "logo",
            "insta",
            "facebook",
            "category",
            "insta_followers",
            "facebook_followers",
            "category",
            "result_number",
            "review_status",
            "reviewed_by",
        )


class MigrateBrandSerializer(serializers.Serializer):
    draft_profiles = serializers.SlugRelatedField(
        slug_field="id", queryset=DraftProfile.objects.all(), required=True, many=True
    )

    def save(self, **kwargs):
        draft_profiles = self.validated_data.get("draft_profiles")
        for profile in draft_profiles:
            category = profile.category
            category = Category.objects.get_or_create(name=category)
            BrandProfile.objects.get_or_create(
                name=profile.brand_name,
                category=category[0],
                description=profile.description,
                insta=profile.insta,
                facebook=profile.facebook,
                # owner = self.request.user
                website=profile.url,
            )
