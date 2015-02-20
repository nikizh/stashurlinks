from stashmarksApp import models
from rest_framework import serializers

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('name',)
