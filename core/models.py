from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

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
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    loyalty_points = models.IntegerField(blank=True, null=True)
    
    # add any additional fields you want for the user profile here
    
    def __str__(self):
        return self.user.username
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'profiles'