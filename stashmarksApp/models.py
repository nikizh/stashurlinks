from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    title = models.CharField(max_length=256)
    url = models.URLField()
    public = models.BooleanField(default=True)
    thumb = models.CharField(max_length=128)
    tags = models.ManyToManyField(Tag)
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.name
