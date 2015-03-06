from stashmarksApp import models
from rest_framework import serializers
from datetime import datetime

class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=25)

    class Meta:
        model = models.Tag
        fields = ('name',)


class BookmarkSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, allow_null=True)

    def create(self, validated_data):

        validated_data['date_created'] = datetime.utcnow()

        # TODO create thumb
        validated_data['thumb'] = 'placeholder.png'

        tags = validated_data.get('tags', validated_data)

        validated_data.pop('tags', None)

        # Create bookmark
        bookmark = models.Bookmark(**validated_data)
        bookmark.save()

        # Add tags to the new bookmark
        for i in range(len(tags)):
            current, success = models.Tag.objects.get_or_create(name=tags[i]["name"])
            bookmark.tags.add(current)

        bookmark.save()

        return bookmark

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.url = validated_data.get('url', instance.url)
        instance.public = validated_data.get('public', instance.public)
        instance.save()

        instance.tags.clear()
        tags = validated_data.get('tags', instance.tags)
        for i in range(len(tags)):
            current, success = models.Tag.objects.get_or_create(name=tags[i]["name"])
            instance.tags.add(current)

        return instance

    class Meta:
        model = models.Bookmark
        fields = ('id', 'title', 'url', 'public', 'thumb', 'tags', 'date_created')