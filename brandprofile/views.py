import json
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from brandprofile.filters import ProfileFilters
from brandprofile.forms import FileUploadForm
from brandprofile.models import BrandProfile, Category
from brandprofile.permissions import IsAuthenticatedOrReadOnlyForList
from brandprofile.serializers import BrandProfileSerializer, CategorySerializer
import pandas as pd
from django_filters.rest_framework import DjangoFilterBackend
from utils.pagination import CustomPageNumberPagination
from django.core.files.uploadedfile import InMemoryUploadedFile

import base64
import io
from PIL import Image


def decodeDesignImage(data):
    try:
        data = base64.b64decode(data.encode("UTF-8"))
        buf = io.BytesIO(data)
        img = Image.open(buf)

        # Convert image to RGB if it has an alpha channel
        if img.mode in ("RGBA", "LA") or (
            hasattr(img, "info") and "transparency" in img.info
        ):
            img = img.convert("RGB")

        return img
    except:
        return None


class BrandProfileViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPageNumberPagination
    queryset = BrandProfile.objects.all()
    serializer_class = BrandProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProfileFilters


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnlyForList]


class UploadCSVView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id="upload_file",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {"file": {"type": "string", "format": "binary"}},
            }
        },
    )
    def post(self, request, format=None):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]  # Get the uploaded file from the form
            if not file:
                return Response({"error": "No file uploaded"}, status=400)
            errors = []
            columns = [
                "company name",
                "website",
                "scrap_title",
                "scrap_desc",
                "insta_url",
                "facebook_url",
                "category",
                "logo_url",
                "tags",
                "Instagram Followers",
                "Facebook Followers",
            ]
            file_name = file.name
            file_extension = file_name.split(".")[-1]
            if file_extension == "xlsx":
                read_file = pd.ExcelFile(file)
                sheet_names = read_file.sheet_names
                if sheet_names:
                    first_sheet_name = sheet_names[0]
                    df = pd.read_excel(read_file, sheet_name=first_sheet_name)
                else:
                    raise Exception("No sheets found in the Excel file.")
            else:
                df = pd.read_csv(file)
            df_json = json.loads(df.to_json(orient="records"))
            if len(df.index) > 5000:
                errors.append("Rows should be less than 5000.")
            missing_column = pd.Index(columns).difference(df.columns).tolist()
            if missing_column:
                missing = ", ".join(missing_column)
                if len(missing_column) == 1:
                    errors.append(f"The '{missing}' column is missing from dataset.")
                else:
                    errors.append(
                        f"The following columns are missing from dataset: {missing}."
                    )
            if errors:
                return Response({"errors": errors}, status=400)
            for entry in df_json:
                print(entry)
                brand = BrandProfile.objects.filter(
                    name=entry["company name"],
                    website=entry["website"],
                    facebook=entry["facebook_url"],
                    insta=entry["insta_url"],
                    # facebook_followers=entry["Facebook Followers"],
                    # insta_followers=entry["Instagram Followers"],
                    # logo=entry["logo_url"],
                )
                if brand.exists():
                    pass
                else:
                    category = Category.objects.get_or_create(name=entry["category"])
                    if not category:
                        return Response(
                            {"errors": entry["category"]},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    new_brand = BrandProfile.objects.create(
                        name=entry["company name"],
                        website=entry["website"],
                        facebook=entry["facebook_url"],
                        insta=entry["insta_url"],
                        logo=entry["logo_url"],
                        search_tags=entry["tags"],
                        category=category[0],
                        owner_id=request.user.id,
                        facebook_followers=entry["Facebook Followers"],
                        insta_followers=entry["Instagram Followers"],
                    )
                    # if entry["logo_url"]:
                    #     img = decodeDesignImage(entry["logo_url"])
                    #     img_io = io.BytesIO()
                    #     img.save(img_io, format="JPEG")
                    #     new_brand.image = InMemoryUploadedFile(
                    #         img_io,
                    #         field_name=None,
                    #         name="token" + ".jpg",
                    #         content_type="image/jpeg",
                    #         size=img_io.tell,
                    #         charset=None,
                    #     )
                    if entry["logo_url"]:
                        check = entry["logo_url"]
                        img = decodeDesignImage(entry["logo_url"])
                        if img:
                            img_io = io.BytesIO()
                            img.save(img_io, format="JPEG")
                            img_io.seek(0)  # Ensure the stream position is at the start
                            new_brand.logo.save(
                                f"{entry['company name']}_logo.jpg",
                                InMemoryUploadedFile(
                                    img_io,
                                    field_name=None,
                                    name=f"{entry['company name']}_logo.jpg",
                                    content_type="image/jpeg",
                                    size=img_io.getbuffer().nbytes,
                                    charset=None,
                                ),
                                save=True,
                            )
                    new_brand.save()
            return Response(
                {"message": "Data Added Successfully"}, status=status.HTTP_201_CREATED
            )
