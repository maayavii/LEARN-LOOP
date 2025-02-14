from django.contrib import admin
from .models import Profile, Relationship
from blog.models import Post, Tag

admin.site.register(Profile)
admin.site.register(Relationship)
admin.site.register(Tag)