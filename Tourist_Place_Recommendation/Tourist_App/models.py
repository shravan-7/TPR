from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

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
    otp = models.CharField(max_length=6, null=True, blank=True)
    user_name = models.CharField(max_length=200, unique=True)
    is_enabled = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    gender = models.IntegerField(choices=[(0, 'Male'), (1, 'Female'), (2, 'Other')])
    category_prefs = models.CharField(max_length=255, default="")
    location_prefs = models.CharField(max_length=255, default="")

    objects = UserManager()

    groups = models.ManyToManyField(Group, related_name="custom_user_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions")

    def __str__(self):
        return self.user_name

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name

class Dataset(models.Model):
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
    sentiment = models.IntegerField(default=1)

    class Meta:
        db_table = "dataset"

    def __str__(self):
        return self.Name

class DatasetLoaded(models.Model):
    is_loaded = models.BooleanField(default=False)
    loaded_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    ratings = models.CharField(max_length=50)
    comments = models.TextField()
    sentiment = models.IntegerField(default=0)

    class Meta:
        db_table = "feedback"

    def __str__(self):
        return f"{self.user.name}'s feedback on {self.place.Name}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Dataset, on_delete=models.CASCADE)

    class Meta:
        db_table = "favorite"
        unique_together = ("user", "place")

    def __str__(self):
        return f"{self.user.name}'s favorite: {self.place.Name}"

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

    def __str__(self):
        return f"{self.user.name}'s review of {self.place.Name}"

class ReviewPhoto(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="photos")
    photo = models.ImageField(upload_to="review_images")

    def __str__(self):
        return f"Photo for {self.review}"
