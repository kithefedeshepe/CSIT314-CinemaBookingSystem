from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role=None):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, role=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# User class

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    ROLE =  (('UserAdmin', 'UserAdmin'),
             ('CinemaOwner', 'CinemaOwner'),
             ('CinemaManager', 'CinemaManager'),
             ('Customer', 'Customer'))
    role = models.CharField(max_length=30, choices=ROLE, default='Customer')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

# Profile class

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    loyalty_points = models.IntegerField(blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
# Movie class

class Movie(models.Model):
    movie_title = models.CharField(max_length=255)
    movie_description = models.TextField()

class Image(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_images')
    image = models.ImageField(upload_to='movie_images/')