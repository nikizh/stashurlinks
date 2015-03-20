import os
import shutil
from stashmarksProj import settings
from stashmarksApp import models
from rest_framework import serializers
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from PIL import Image
import hashlib


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5'
capabilities = dict(webdriver.DesiredCapabilities.PHANTOMJS)
capabilities['phantomjs.page.settings.userAgent'] = user_agent
capabilities['phantomjs.page.settings.loadImages'] = 'true'
capabilities['phantomjs.page.settings.webSecurityEnabled'] = 'false'


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=25)

    class Meta:
        model = models.Tag
        fields = ('name',)


class BookmarkSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, allow_null=True)
    liked = serializers.SerializerMethodField(read_only=True)

    def get_liked(self, obj):
        request = self.context.get('request', None)
        user = request.user
        try:
            current = models.Ratings.objects.get(owner=user, bookmark=obj)
            return current.liked
        except models.Ratings.DoesNotExist:
            pass
        return False

    def create(self, validated_data):

        validated_data['date_created'] = datetime.utcnow()

        hash_object = hashlib.sha1()

        url = validated_data.get('url', validated_data)
        hash_object.update(url.encode())

        name = hash_object.hexdigest()[:7] + '.png'
        validated_data['thumb'] = name

        file_name = os.path.join(settings.THUMBS_PATH, name)

        try:
            driver = webdriver.PhantomJS(desired_capabilities=capabilities)
            driver.set_window_size(1024, 768)

            driver.get(url)
            driver.save_screenshot(file_name)
            im = Image.open(file_name)
            im = im.crop((0, 0, 1024, 768))
            im.thumbnail([300, 300], Image.ANTIALIAS)
            im.save(file_name, quality=100)
        except WebDriverException:
            placeholder_file_name = os.path.join(settings.THUMBS_PATH, 'placeholder.png')
            shutil.copy(placeholder_file_name, file_name)

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
        fields = ('id', 'title', 'url', 'public', 'thumb', 'tags', 'date_created', 'likes', 'liked')


class RatingsSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    def get_likes(self, obj):
        return obj.bookmark.likes

    class Meta:
        model = models.Ratings
        fields = ('liked','likes')
