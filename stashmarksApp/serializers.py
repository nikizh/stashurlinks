from rest_framework.relations import PrimaryKeyRelatedField
from stashmarksApp import models
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('name',)


class BookmarkSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, allow_null=True)

    class Meta:
        model = models.Bookmark
        fields = ('id', 'title', 'url', 'public', 'thumb', 'tags', 'date_created')