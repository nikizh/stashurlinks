import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stashmarksProj.settings')

import django
django.setup()

import django.db.utils
import datetime
import random
from django.contrib.auth.models import User
from stashmarksApp.models import Bookmark, Tag
from populate_sample_data import SAMPLE_DATA


def populate():
    users = create_users()

    for i in range(0, 4):
        populate_user_data(users[i], SAMPLE_DATA[i])


def populate_user_data(user, data):
    """
    Populates data to the account of the given user

    :type user: User
    """

    for item in data:
        value = data[item]

        bookmark, created = Bookmark.objects.get_or_create(
            title=value['title'],
            url=value['url'],
            public=value['is_public'],
            thumb=value['thumb'],
            owner=user)

        if created:
            date_created = datetime.datetime.now() + datetime.timedelta(days=-random.randint(0, 10), hours=-random.randint(0, 12))
            bookmark.date_created = date_created

            tags = get_or_create_tags(value['tags'])

            for tag in tags:
                bookmark.tags.add(tag)

            bookmark.save()


def get_or_create_tags(tags):
    tag_items = []

    for tag in tags:
        tag_item, created = Tag.objects.get_or_create(name=tag)
        tag_items.append(tag_item)

    return tag_items


def create_or_get_user(username, email, password):
    try:
        return User.objects.create_user(username, email, password)
    except django.db.utils.IntegrityError:
        return User.objects.get_by_natural_key(username)


def create_users():
    # Create administrator
    try:
        User.objects.create_superuser('admin', 'admin@example.com', 'pass')
    except django.db.utils.IntegrityError:
        pass

    user1 = create_or_get_user('user1', 'user1@example.com', 'pass')
    user2 = create_or_get_user('user2', 'user2@example.com', 'pass')
    user3 = create_or_get_user('user3', 'user3@example.com', 'pass')
    user4 = create_or_get_user('user4', 'user4@example.com', 'pass')

    return [user1, user2, user3, user4]


# Start execution here!
if __name__ == '__main__':
    print("Starting population script...")
    populate()
