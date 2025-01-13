from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.core.exceptions import ValidationError

User = get_user_model() # model of current user 
# Create your models here.

# diff tables as classes and rows and variables
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True) # might leave it blank 
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png') # 2 types of images
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    print("uploading done .....",image)
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def get_image_url(self):
        """Safe method to get image URL"""
        try:
            return self.image.url if self.image else None
        except (ValueError, AttributeError):
            return None
    @property
    def image_url(self):
        return self.get_image_url()

    def clean(self):
        """Validate image field"""
        if self.image:
            try:
                # This will raise ValueError if file is missing
                self.image.url
            except ValueError:
                raise ValidationError('Image file is missing')

    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user