from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    is_modaretor = models.BooleanField(default=True)
    otp = models.CharField(max_length=8, null=True, blank=True)
    is_password_forget = models.BooleanField(default=False)
    profile_images = models.ImageField(
        upload_to="user_profiles",
        storage=MediaCloudinaryStorage(),
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username
    
