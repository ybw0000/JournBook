from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(verbose_name='username', max_length=30, unique=True)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    first_name = models.CharField(verbose_name='first name', max_length=30)
    last_name = models.CharField(verbose_name='last name', max_length=30)
    biography = models.TextField(verbose_name='biography', max_length=1000)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


FOLLOW_CHOISES = (
    ('Follow', 'Follow'),
    ('Unfollow', 'Unfollow')
)


class UserFollow(models.Model):
    following_id = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follower_id = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    value = models.CharField(choices=FOLLOW_CHOISES, default='Follow', max_length=10000)

    def __str__(self):
        return self.following_id.username
