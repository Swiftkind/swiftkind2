import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import password_validation

from wagtail.snippets.models import register_snippet



def upload_avatar_to(instance, filename):
    filename, ext = os.path.splitext(filename)
    return os.path.join(
        'avatar_images',
        '{user}/{file}/'.format(user=instance.id, file=filename)
    )


class UserManager(BaseUserManager):
    """ A custom user manager to deal with email as username
    """

    def create_user(self, email, password, **extra_fields):
        # Create and saves a User with the given email and password.
        if not email:
            raise ValueError('Email is required.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        # Create and save a superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


@register_snippet
class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model
    """
    MANAGEMENT = '0'
    DEVELOPER = '1'
    DESIGNER = '2'
    TRAINEE = '3'
    STAFF = '4'

    POSITION_TYPE = (
        (DEVELOPER, 'developer'),
        (DESIGNER, 'designer'),
        (TRAINEE, 'trainee'),
        (MANAGEMENT, 'management'),
        (STAFF, 'staff'),
    )

    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=72, blank=True, null=True)
    last_name = models.CharField(max_length=72, blank=True, null=True)
    position = models.CharField(max_length=1, choices=POSITION_TYPE, default=DEVELOPER)
    avatar = models.ImageField(
        verbose_name=_('profile picture'),
        null=True,
        upload_to=upload_avatar_to,
        blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text = _('Designates whether this user is active'),
    )
    is_superuser = models.BooleanField(
        _('super user'),
        default=False,
        help_text="Designates whether the user is super user or site admin")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects  = UserManager()

    def __str__(self):
        return "{}".format(self.email)

    @property
    def fullname(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return "{}".format(self.email)

    def position_verbose(self):
        return dict(User.POSITION_TYPE)[self.position]
