from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser


def user_dir_file(instance, image_file, *args, **kwargs):
    print(instance.category)
    return "user_{0}/{1}".format(instance.category, image_file)


def category_dir_file(instance, image_file, *args, **kwargs):
    return "category_{0}/{1}".format(instance.category_of_photo, image_file)


class User(AbstractUser):
    email = models.EmailField(
        max_length=255,
        unique=True
    )
    avatar = models.ImageField(
        upload_to="",
        null=True,
        default='default/avatar.svg'
    )
    bio = models.TextField(
        null=True, blank=True
    )

    facebook_link = models.URLField(
        max_length=200,
        null=True,
        blank=True
    )
    twitter_link = models.URLField(
        max_length=200,
        null=True,
        blank=True
    )
    instagram_link = models.URLField(
        max_length=200,
        null=True,
        blank=True
    )
    other_link = models.URLField(
        max_length=200,
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_absolute_url(self):
        return reverse("profile", args=[f'{str(self.first_name)}-{str(self.last_name)}'])


class Category(models.Model):
    category_of_photo = models.CharField(
        max_length=20, unique=True
    )
    descriptive_photo = models.ImageField(
        upload_to=category_dir_file, max_length=150, null=True, blank=True
    )

    def __str__(self):
        return self.category_of_photo

    class Meta:
        verbose_name_plural = "Categories"


class PhotoGraphy(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='project')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(
        max_length=150,
        unique=True,
    )
    description = models.TextField()
    photo = models.ImageField(upload_to=user_dir_file, max_length=150, help_text="your picture")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} {self.title}"

    class Meta:
        verbose_name_plural = "Photography"
