# Generated by Django 5.0.3 on 2024-04-16 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("draft_profile", "0004_draftprofile_review_status_draftprofile_reviewed_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="draftprofile",
            name="logo",
            field=models.ImageField(blank=True, null=True, upload_to="draft/"),
        ),
    ]
