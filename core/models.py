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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='profiles')
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    loyalty_points = models.PositiveIntegerField(default = 0)
    
    def __str__(self):
        return self.name
    
    
class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie_title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    duration = models.DurationField()
    release_date = models.DateField()
    cast = models.CharField(max_length=200)
    director = models.CharField(max_length=50)
    movie_description = models.TextField()
     
    def formatted_duration(self):
        hours, minutes = self.duration.total_seconds() // 3600, \
                                  (self.duration.total_seconds() // 60) % 60
        return f"{int(hours)}h {int(minutes)}m"
    
    def __str__(self):
        return self.movie_title
    

class MovieImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  
       
class CinemaRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
    
class MovieSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='sessions')
    session_date = models.DateField()
    cinema_room = models.ForeignKey(CinemaRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name='cinemaroom')

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
        return f"{self.movie.movie_title}-{self.session_date}-{self.session_time}-{self.cinema_room.name}"


class FoodandBeverage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.CharField(max_length=100)
    menu_description = models.TextField()
    price = models.FloatField() 
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.menu} - {self.menu_description}"

    class Meta:
        verbose_name_plural = 'Foods and Beverages'   
 
class FoodandBeverageImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = models.TextField()
    FnB = models.ForeignKey(FoodandBeverage, on_delete=models.CASCADE)  


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking_owner = models.ForeignKey(User, on_delete=models.CASCADE) 
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE, related_name='sessions')
    
    TICKET_TYPE = (('Adult', 'Adult'),
             ('Senior', 'Senior'),
             ('Child', 'Child'))
    
    ticket_type = models.CharField(max_length=30, choices=TICKET_TYPE, default='Adult')
    seat_number = models.CharField(max_length=30)
    FnB = models.ForeignKey(FoodandBeverage, on_delete=models.CASCADE, related_name='foodandbeverage') 
    
    price = models.FloatField(default=0) 

    def get_ticket_price(self):
        if self.ticket_type == 'Adult':
            return 10
        elif self.ticket_type == 'Senior':
            return 8
        elif self.ticket_type == 'Child':
            return 6
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.get_ticket_price()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.movie_session}X{self.ticket_type}-{self.seat_number}"

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report_description = models.TextField()
