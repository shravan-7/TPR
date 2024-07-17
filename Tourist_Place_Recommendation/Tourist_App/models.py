from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):

    def create_user(self, email, name, password=None, **extra_fields):

        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "user_name"
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    address = models.TextField()
    otp = models.CharField(max_length=6, null=True)
    user_name = models.CharField(max_length=200, unique=True)
    is_enabled = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    gender = models.IntegerField()
    category_prefs = models.CharField(max_length=255, default="")
    location_prefs = models.CharField(max_length=255, default="")
    objects = UserManager()
    groups = models.ManyToManyField(Group, related_name="custom_user_groups")
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions"
    )


class Category(models.Model):
    class Meta:
        db_table = "category"

    name = models.IntegerField(blank=False, default=None)


class Dataset(models.Model):
    class Meta:
        db_table = "dataset"

    ID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=255)
    City = models.CharField(max_length=100)
    Category = models.CharField(max_length=100)
    Ratings = models.DecimalField(max_digits=3, decimal_places=1)
    Rating_count = models.CharField(max_length=255)
    Description = models.TextField()
    Address = models.CharField(max_length=255)
    Map_link = models.URLField(max_length=500)
    Review_1 = models.TextField(default="")
    Review_2 = models.TextField(default="")
    Review_3 = models.TextField(default="")
    openingHours_0_day = models.CharField(max_length=200, default="")
    openingHours_0_hours = models.CharField(max_length=200, default="")
    openingHours_1_day = models.CharField(max_length=200, default="")
    openingHours_1_hours = models.CharField(max_length=200, default="")
    openingHours_2_day = models.CharField(max_length=200, default="")
    openingHours_2_hours = models.CharField(max_length=200, default="")
    openingHours_3_day = models.CharField(max_length=200, default="")
    openingHours_3_hours = models.CharField(max_length=200, default="")
    openingHours_4_day = models.CharField(max_length=200, default="")
    openingHours_4_hours = models.CharField(max_length=200, default="")
    openingHours_5_day = models.CharField(max_length=200, default="")
    openingHours_5_hours = models.CharField(max_length=200, default="")
    openingHours_6_day = models.CharField(max_length=200, default="")
    openingHours_6_hours = models.CharField(max_length=200, default="")
    sentiment = models.IntegerField(blank=False, default=1)


class Feedback(models.Model):
    class Meta:
        db_table = "feedback"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    ratings = models.CharField(blank=False, max_length=50)
    comments = models.TextField()
    sentiment = models.IntegerField(blank=False, default=None)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    class Meta:
        db_table = "favorite"  # Specify a unique table name for FavoritePlace
        unique_together = ("user", "place")


class Review(models.Model):
    RATING_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    place = models.ForeignKey(Dataset, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    with_whom = models.CharField(max_length=100)
    review_text = models.TextField()


class ReviewPhoto(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="photos")
    photo = models.ImageField(upload_to="review_images")
