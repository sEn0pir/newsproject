from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):

        post_rating = self.post_set.aggregate(post_rating_sum=Sum('rating'))['post_rating_sum'] or 0
        post_rating *= 3


        comment_rating = self.user.comment_set.aggregate(comment_rating_sum=Sum('rating'))['comment_rating_sum'] or 0


        post_comment_rating = Comment.objects.filter(post__author=self).aggregate(post_comment_rating_sum=Sum('rating'))['post_comment_rating_sum'] or 0


        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Article'),
        (NEWS, 'News'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    post_type = models.CharField(
        max_length=2,
        choices=POST_TYPES,
        default=NEWS
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_post_type_display()}: {self.title}"

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post.title} - {self.category.name}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        permissions = [
            ("add_post", "Can add post"),
            ("change_post", "Can change post"),
            ("delete_post", "Can delete post"),
        ]

from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name="common")
        instance.groups.add(group)

from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name="subscribed_categories")

    def __str__(self):
        return self.name
