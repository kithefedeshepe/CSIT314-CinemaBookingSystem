from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ROLE = (
        ('UserAdmin', 'UserAdmin'),
        ('CinemaManager', 'CinemaManager'),
        ('Customer', 'Customer'),
        ('CinemaOwner', 'CinemaOwner'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLE, default='Customer')

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            Profile.objects.create(user=self)
        
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user.username} Profile"