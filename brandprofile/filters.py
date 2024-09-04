from django_filters import rest_framework as filters
from brandprofile.models import BrandProfile


class ProfileFilters(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    category = filters.CharFilter(field_name="category__name", lookup_expr="icontains")
    rating = filters.NumberFilter(field_name="brandprofile_rating__rating")
    rating_min = filters.NumberFilter(
        field_name="brandprofile_rating__rating", lookup_expr="gte"
    )
    rating_max = filters.NumberFilter(
        field_name="brandprofile_rating__rating", lookup_expr="lte"
    )

    class Meta:
        model = BrandProfile
        fields = ["name", "category", "rating", "rating_min", "rating_max"]

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        rating_min = self.data.get("rating_min")
        rating_max = self.data.get("rating_max")

        if rating_min or rating_max:
            queryset = queryset.filter(
                brandprofile_rating__rating__gte=rating_min,
                brandprofile_rating__rating__lte=rating_max,
            ).distinct()

        return queryset
