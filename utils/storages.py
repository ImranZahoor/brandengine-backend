from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION
    # default_acl = None  # Remove the ACL setting


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False
    default_acl = None  # Remove the ACL setting


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = None  # Remove the ACL setting
    file_overwrite = False
    custom_domain = False
