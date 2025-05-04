from django.db import models
from users.models import CustomUser
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.

class Category(models.Model):
    category = models.CharField(unique=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.category


class News365(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    head_lines = models.CharField(max_length=200)
    discriptions = models.TextField()
    image1 = models.ImageField(upload_to="news", null=True, blank=True, storage=MediaCloudinaryStorage())
    image2 = models.ImageField(upload_to="news", null=True, blank=True, storage=MediaCloudinaryStorage())
    image3 = models.ImageField(upload_to="news", null=True, blank=True, storage=MediaCloudinaryStorage())
    video = models.TextField(null=True, blank=True)  # for youtube videos
    adverticement = models.ImageField(upload_to='adverticement', storage=MediaCloudinaryStorage(), null=True, blank=True)
    is_impotent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.head_lines
