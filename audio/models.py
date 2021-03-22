from django.db import models
from tp.models import UUIDAsIDModel
from django.contrib.auth.models import User
from django.utils.text import slugify
from tp.storage_backends import PublicImageStorage, PublicMP3Storage
from .choices import LICENSE_CHOICES, get_license_info
import string, random


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


def slugify_file_name(instance, filename):
    fname, dot, extension = filename.rpartition('.')
    slug = slugify(fname)
    return f'{slug}.{extension}'


class EpisodeAndFeed(UUIDAsIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=False)

    image = models.ImageField(
        storage=PublicImageStorage(),
        upload_to=slugify_file_name,
        null=True, blank=True)

    image_license = models.SmallIntegerField(
        choices=LICENSE_CHOICES,
        default=2,
    )

    image_title = models.CharField(max_length=255, default='')
    image_attribution = models.CharField(max_length=255, default='')
    image_attribution_url = models.URLField(max_length=255, blank=True)
    original_image_url = models.URLField(max_length=255, default='')
    image_license_jurisdiction = models.TextField(null=False, default='(no jurisdiction specified)')

    @property
    def image_license_name(self):
        return(get_license_info(self.image_license))[0]

    @property
    def image_license_url(self):
        return(get_license_info(self.image_license))[1]

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + self.title)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Feed(EpisodeAndFeed):
    author_url = models.URLField(max_length=255, default='')
    ebook_title = models.CharField(max_length=255, default='')
    ebook_url = models.URLField(max_length=255, default='')
    translator = models.CharField(max_length=255, blank=True)
    translator_url = models.URLField(max_length=255, blank=True)
    intro_author = models.CharField(max_length=255, blank=True)
    intro_author_url = models.URLField(max_length=255, blank=True)
    license_jurisdiction = models.TextField(blank=True, default='(no jurisdiction specified)')
    license = models.SmallIntegerField(
        choices=LICENSE_CHOICES,
        default=1,
    )

    @property
    def license_name(self):
        return(get_license_info(self.license))[0]

    @property
    def license_url(self):
        return(get_license_info(self.license))[1]


class Episode(EpisodeAndFeed):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    pub_date = models.DateField()
    episode_number = models.IntegerField(null=True)

    mp3 = models.FileField(
        storage=PublicMP3Storage(),
        upload_to=slugify_file_name,
        null=True, blank=True)
