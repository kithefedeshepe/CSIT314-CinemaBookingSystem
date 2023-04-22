from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    loyalty_points = models.PositiveIntegerField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    
class Movie(models.Model):
    movie_title = models.CharField(max_length=50, primary_key=True)
    genre = models.CharField(max_length=50)
    duration = models.DurationField()
    release_date = models.DateField()
    cast = models.CharField(max_length=200)
    director = models.CharField(max_length=50)
    movie_description = models.TextField()
    movie_img = models.ImageField(upload_to='movie_images/', blank=True)

    def formatted_duration(self):
        hours, minutes = self.duration.total_seconds() // 3600, \
                                  (self.duration.total_seconds() // 60) % 60
        return f"{int(hours)}h {int(minutes)}m"
    
    def __str__(self):
        return self.movie_title

    def get_first_image_url(self):
        if self.movie_img:
            return self.movie_img.url
        else:
            return None


class CinemaRoom(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
    
class MovieSession(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='sessions')
    session_date = models.DateField()
    room_choices = [(room.id, room.name) for room in CinemaRoom.objects.all()]
    cinemaroom = models.ForeignKey(CinemaRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name='cinemaroom', choices=room_choices)
    
    TIME = (
        ('08:30', '08:30'),
        ('11:30', '11:30'),
        ('14:00', '14:00'),
        ('16:30', '16:30'),
        ('17:50', '17:50'),
        ('18:40', '18:40'),
        ('19:30', '19:30'),
        ('20:40', '20:40'),
        ('21:10', '21:10'),
    )
    session_time = models.CharField(choices=TIME, max_length=10)

    def __str__(self):
        return f"{self.movie.movie_title} - {self.session_date}"
