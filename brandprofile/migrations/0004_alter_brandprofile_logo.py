# Generated by Django 5.0.3 on 2024-03-22 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("brandprofile", "0003_brandprofile_address_brandprofile_city"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brandprofile",
            name="logo",
            field=models.ImageField(blank=True, null=True, upload_to="logo/"),
        ),
    ]
