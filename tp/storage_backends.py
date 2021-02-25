from storages.backends.s3boto3 import S3Boto3Storage
# from django.conf import settings


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class PublicMP3Storage(S3Boto3Storage):
    location = 'mp3'
    default_acl = 'public-read'
    # file_overwrite = False


class PublicImageStorage(S3Boto3Storage):
    location = 'images'
    default_acl = 'public-read'
