from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username.capitalize()


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    thumbnail = models.ImageField()
    publish_date = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("details", kwargs={
            "slug":self.slug
        })

    def get_like_url(self):
        return reverse("like", kwargs={
            "slug":self.slug
        })
        
    def comments(self):
        return self.comment_set.all()

    def get_like_count(self):
        return self.like_set.all().count()

    def get_comment_count(self):
        return self.comment_set.all().count()

    def get_view_count(self):
        return self.postview_set.all().count()

    def __str__(self):
        return self.title.capitalize()


class Comment(models.Model):
    content = models.TextField()
    timestamp = models.DateField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username.capitalize()}'s comment"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username.capitalize()}'s like"


class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Seen by {self.user.username}"