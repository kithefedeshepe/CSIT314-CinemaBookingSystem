from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


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

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='profiles')
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    loyalty_points = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    def email(self):
        return self.user.email