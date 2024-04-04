import json

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from brandprofile.forms import FileUploadForm
from draft_profile.models import DraftProfile
import pandas as pd

from draft_profile.serializers import DraftProfileSerializer, MigrateBrandSerializer


class DraftProfileViewSet(viewsets.ModelViewSet):
    queryset = DraftProfile.objects.all()
    serializer_class = DraftProfileSerializer
    permission_classes = [IsAuthenticated]

    def migrate_brands(self, request):
        serializer = MigrateBrandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": serializer.data, "message": "Data Migrated Successfully"},
            status=status.HTTP_201_CREATED,
        )


class UploadCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]  # Get the uploaded file from the form
            if not file:
                return Response({"error": "No file uploaded"}, status=400)
            errors = []
            columns = [
                "Level 3 Category",
                "Query",
                "Title",
                "Description",
                "URL",
                "Brand Name",
                "Result Number",
                "Associated Instagram",
                "Facebook URL",
                "Instagram Followers",
                "Facebook Followers",
                "Logo",
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
                drafts = DraftProfile.objects.filter(
                    brand_name=entry["Brand Name"],
                    title=entry["Title"],
                    query=entry["Query"],
                    url=entry["URL"],
                    insta=entry["Associated Instagram"],
                    facebook=entry["Facebook URL"],
                )
                if drafts.exists():
                    pass
                else:
                    new_draft = DraftProfile.objects.create(
                        brand_name=entry["Brand Name"],
                        title=entry["Title"],
                        query=entry["Query"],
                        url=entry["URL"],
                        insta=entry["Associated Instagram"],
                        facebook=entry["Facebook URL"],
                        category=entry["Level 3 Category"],
                        description=entry["Description"],
                        insta_followers=entry["Instagram Followers"],
                        facebook_followers=entry["Facebook Followers"],
                        logo=entry["Logo"],
                        result_number=entry["Result Number"],
                    )
                    new_draft.save()
            return Response(
                {"message": "Data Added Successfully"}, status=status.HTTP_200_OK
            )


class MigrateBrands(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = MigrateBrandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": serializer.data, "message": "Data Migrated Successfully"},
            status=status.HTTP_201_CREATED,
        )
