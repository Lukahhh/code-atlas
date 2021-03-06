from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template import loader
from django.db import models


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    """
    Custom User model with email rather than username. 
    """
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_recent_searches(self):
        searches = self.search_history.order_by('-search_date').values('query')[:5]
        return searches

# @receiver(post_save, sender=User)
# def send_welcome_email(sender, instance, created, **kwargs):
#     """
#     Send a new User a welcome email.
#     """
#     if created:
#         subject = 'Welcome to Code Atlas'
#         body = 'Welcome to Code Atlas'

#         email_message = EmailMultiAlternatives(
#             subject, 
#             body, 
#             'noreply@code-atlas.me', 
#             [instance.email]
#         )
#         html_email = loader.render_to_string('email/welcome.html')
#         email_message.attach_alternative(html_email, 'text/html')
#         email_message.send()