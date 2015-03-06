from stashmarksApp import models
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=25)
    class Meta:
        model = models.Tag
        fields = ('name',)


class BookmarkSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, allow_null=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.url = validated_data.get('url', instance.url)
        instance.public = validated_data.get('public', instance.public)


        instance.save()
        tags = validated_data.get('tags', instance.tags)
        for i in range(len(tags)):
            instance.tags.add(models.Tag.objects.get_or_create(name=tags[i]["name"]))


        return instance

    class Meta:
        model = models.Bookmark
        fields = ('id', 'title', 'url', 'public', 'thumb', 'tags', 'date_created')