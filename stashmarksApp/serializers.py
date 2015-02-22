from rest_framework.relations import PrimaryKeyRelatedField
from stashmarksApp import models
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'name', 'date_created')

class BookmarkSerializer(serializers.ModelSerializer):
    tags = PrimaryKeyRelatedField(many=True, queryset=models.Tag.objects.all(), allow_null=True)

    class Meta:
        model = models.Bookmark
        fields = ('id','title','url','public','thumb','tags','date_created')