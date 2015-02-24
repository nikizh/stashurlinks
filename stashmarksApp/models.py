from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField()
    owner = models.ForeignKey(User)
    date_created = models.DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'slug', 'owner')


class Bookmark(models.Model):
    title = models.CharField(max_length=256)
    url = models.URLField()
    public = models.BooleanField(default=True)
    thumb = models.CharField(max_length=128)
    tags = models.ManyToManyField(Tag)
    owner = models.ForeignKey(User)
    date_created = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.url
