from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)


from django.contrib.auth.models import Group

authors_group, _ = Group.objects.get_or_create(name="authors")
authors_group.permissions.set([
    "news.add_post",
    "news.change_post",
    "news.delete_post",
])


from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Post


authors_group, created = Group.objects.get_or_create(name="authors")


content_type = ContentType.objects.get_for_model(Post)
permissions = Permission.objects.filter(content_type=content_type)


authors_group.permissions.set(permissions)

from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    search_fields = ("title", "author__user__username")

from django.contrib import admin
from django.contrib.auth.models import Group

authors_group = Group.objects.get(name="authors")
authors_group.permissions.set([
    "add_post",
    "change_post",
])
