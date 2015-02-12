from django.contrib import admin
from stashmarksApp import models


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(models.Tag, TagAdmin)
