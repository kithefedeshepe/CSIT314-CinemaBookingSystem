from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
import uuid

# Custom admin
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

# Custom user
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
    
    def usercreate(self, username, password, email, role, *args, **kwargs):
        self.username = username
        self.email = email
        self.role = role
        if password is not None:
            self.password = make_password(password)
        super().save(*args, **kwargs)
    
    def userupdate(self, email, password, *args, **kwargs):
        if email is not None:
            self.email = email
        if password is not None:
            self.password = make_password(password)
        super().save(*args, **kwargs)
    
    def userdelete(self, *args, **kwargs):
        super(User, self).delete(*args, **kwargs)

    def userauthenticate(self, request, username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)   
        else:
            token = None
        return token

    def userget(self, username):
        return User.objects.get(username = username)
    
    @classmethod
    def usersearch(cls, keyword):
        return cls.objects.filter(username__icontains=keyword)
    
    @classmethod
    def userall(cls):
        return cls.objects.all()
    
    def userlogout(self, request):
        logout(request)
    

# User profile
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='profiles')
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    loyalty_points = models.PositiveIntegerField(default = 0)
    
    def __str__(self):
        return self.name
    
    def profilecreate(self, user, name, dob, *args, **kwargs):
        self.user = user
        self.name = name
        self.date_of_birth = dob
        super().save(*args, **kwargs)
    
    @classmethod
    def profileall(cls):
        return cls.objects.all()
    
    def profileupdate(self, name, date_of_birth, *args, **kwargs):
        if name is not None:
            self.name = name
        if date_of_birth is not None:
            self.date_of_birth = date_of_birth
        super().save(*args, **kwargs)
    
    def profiledelete(self, *args, **kwargs):
        super(Profile, self).delete(*args, **kwargs)
    
    def profileget(self, id):
        return Profile.objects.get(id=id)
    
    @classmethod
    def profilesearch(cls, keyword):
        return cls.objects.filter(Q(user__username__icontains=keyword) | Q(name__icontains=keyword))


# Movie   
class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie_title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    duration = models.DurationField()
    release_date = models.DateField()
    cast = models.CharField(max_length=200)
    director = models.CharField(max_length=50)
    movie_description = models.TextField()
    posterIMG = models.TextField()
    featureIMG = models.TextField()
    
    def formatted_duration(self):
        hours, minutes = self.duration.total_seconds() // 3600, \
                                  (self.duration.total_seconds() // 60) % 60
        return f"{int(hours)}h {int(minutes)}m"
    
    def __str__(self):
        return self.movie_title
    
    def moviecreate(self, movie_title, genre, duration, release_date, cast, director, movie_description, posterIMG, featureIMG, *args, **kwargs):
        self.movie_title = movie_title
        self.genre = genre
        self.duration = duration
        self.release_date = release_date
        self.cast = cast
        self.director = director
        self.movie_description = movie_description
        self.posterIMG = posterIMG
        self.featureIMG = featureIMG
        super().save(*args, **kwargs)
    
    @classmethod
    def movieall(cls):
        return cls.objects.all()
    
    def movieupdate(self, genre, duration, release_date, cast, director, movie_description, posterIMG, featureIMG, *args, **kwargs):
        if genre is not None:
            self.genre = genre
        if duration is not None:
            self.duration = duration
        if release_date is not None:
            self.release_date = release_date
        if cast is not None:
            self.cast = cast
        if director is not None:
            self.director = director
        if movie_description is not None:
            self.movie_description = movie_description
        if posterIMG is not None:
            self.posterIMG = posterIMG
        if featureIMG is not None:
            self.featureIMG = featureIMG
        super().save(*args, **kwargs)
    
    def moviedelete(self, *args, **kwargs):
        super(Movie, self).delete(*args, **kwargs)
    
    def movieget(self, movie_title):
        return Movie.objects.get(movie_title=movie_title)
    
    @classmethod
    def moviesearch(cls, keyword):
        return cls.objects.filter(movie_title__icontains=keyword)

# Cinema room     
class CinemaRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    def cinemaroomcreate(self, name, capacity, *args, **kwargs):
        self.name = name
        self.capacity = capacity
        super().save(*args, **kwargs)
    
    def cinemaroomupdate(self, capacity, *args, **kwargs):
        if capacity is not None:
            self.capacity = capacity
        super().save(*args, **kwargs)
    
    def cinemaroomdelete(self, *args, **kwargs):
        super(CinemaRoom, self).delete(*args, **kwargs)


    def cinemaroomget(self, name):
        return CinemaRoom.objects.get(name = name)
    
    @classmethod
    def cinemaroomsearch(cls, keyword):
        return cls.objects.filter(name__icontains=keyword)
    
    @classmethod
    def cinemaroomall(cls):
        return cls.objects.all()
    
# Movie session
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
        return f"{self.movie.movie_title}-{self.session_date}-{self.session_time}"
    
    def moviesessioncreate(self, movie, session_date, cinema_room, session_time, *args, **kwargs):
        self.movie = movie
        self.session_date = session_date
        self.cinema_room = cinema_room
        self.session_time = session_time
        super().save(*args, **kwargs)
    
    def moviesessionupdate(self, session_date, session_time, *args, **kwargs):
        if session_date is not None:
            self.session_date = session_date
        if session_time is not None:
            self.session_time = session_time
        super().save(*args, **kwargs)
    
    def moviesessiondelete(self, *args, **kwargs):
        super(MovieSession, self).delete(*args, **kwargs)


    def moviesessionget(self, id):
        return MovieSession.objects.get(pk = id)
    
    @classmethod
    def moviesessionsearch(cls, keyword):
        return cls.objects.filter(Q(movie__movie_title__icontains=keyword) | Q(session_date__icontains=keyword)| Q(session_time__icontains=keyword)| Q(cinema_room__name__icontains=keyword))
    
    @classmethod
    def moviesessionall(cls):
        return cls.objects.all()

# Fnb
class FoodandBeverage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.CharField(max_length=100)
    menu_description = models.TextField()
    price = models.FloatField() 
    menuIMG = models.TextField()
    
    def __str__(self):
        return f"{self.menu} - {self.menu_description}"

    def fnbcreate(self, menu, menu_description, price, menuIMG, *args, **kwargs):
        self.menu = menu
        self.menu_description = menu_description
        self.price = price
        self.menuIMG = menuIMG
        super().save(*args, **kwargs)
    
    def fnbupdate(self, price, *args, **kwargs):
        if price is not None:
            self.price = price
        super().save(*args, **kwargs)
    
    def fnbdelete(self, *args, **kwargs):
        super(FoodandBeverage, self).delete(*args, **kwargs)


    def fnbget(self, id):
        return FoodandBeverage.objects.get(pk = id)
    
    @classmethod
    def fnbsearch(cls, keyword):
        return cls.objects.filter(menu__icontains=keyword)
    
    @classmethod
    def fnball(cls):
        return cls.objects.all()
      

# Booking
class MovieBooking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking_owner = models.ForeignKey(User, on_delete=models.CASCADE) 
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE, related_name='sessions')
    
    TICKET_TYPE = (('Adult', 'Adult'),
             ('Senior', 'Senior'),
             ('Child', 'Child'))
    
    ticket_type = models.CharField(max_length=30, choices=TICKET_TYPE, default='Adult')
    seat_number = models.CharField(max_length=30)
    
    def get_ticket_price(self):
        if self.ticket_type == 'Adult':
            return 10
        elif self.ticket_type == 'Senior':
            return 8
        elif self.ticket_type == 'Child':
            return 6

    def str(self):
        return f"{self.movie_session}X{self.ticket_type}-{self.seat_number}"

    def movieBookingCreate(self, booking_owner, movie_session, ticket_type, seat_number, *args, **kwargs):
        if not self.price:
            self.price = self.get_ticket_price()
        self.booking_owner = booking_owner
        self.movie_session = movie_session
        self.ticket_type = ticket_type
        self.seat_number = seat_number
        super().save(*args, **kwargs)

    @classmethod
    def bookingall(cls):
        return cls.objects.all()

    def bookingDelete(self, *args, **kwargs):
        super(MovieBooking, self).delete(*args, **kwargs)

    def movieBookingUpdate(self, seat_number, *args, **kwargs):
        if seat_number is not None:
            self.seat_number = seat_number
        super().save(*args, **kwargs)

    def bookingGet(self, id):
        return MovieBooking.objects.get(pk = id)
    
    @classmethod
    def movieBookSearch(cls, keyword):
        return cls.objects.filter(ticket_type__icontains=keyword)
    
    @property
    def price(self):
        return self.get_ticket_price()
    

# Pre-order fnb   
class FnBBooking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(FoodandBeverage, on_delete=models.CASCADE)
    
    def get_menu_price(self):
        return self.menu.price
    
    def save(self, *args, **kwargs):
        if not self.menu_price:
            self.menu_price = self.get_menu_price()
        super().save(*args, **kwargs)

    @property
    def menu_price(self):
        return self.get_menu_price()

    def __str__(self):
        return f"{self.menu}X{self.menu_price}"
    
    def FnBBookingCreate(self, booking_owner, menu, *args, **kwargs):
        self.booking_owner = booking_owner
        self.menu = menu
        super().save(*args, **kwargs)

    @classmethod
    def FnBBookingall(cls):
        return cls.objects.all()
    
    def fnbbookingGet(self, id):
        return FnBBooking.objects.get(pk = id)


# Report (cinema owner)
class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report_description = models.TextField()
