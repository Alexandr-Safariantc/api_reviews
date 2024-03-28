from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api_yamdb.settings import (
    SLUG_FIELD_MAX_LENGTH,
    USERNAME_FIELD_MAX_LENGTH,
)
from .validators import check_username_for_me_value


class User(AbstractUser):
    """Describes user model."""

    class Roles(models.TextChoices):
        USER = 'user', 'user'
        MODERATOR = 'moderator', 'moderator'
        ADMIN = 'admin', 'admin'

    bio = models.TextField(
        blank=True,
        default='',
        verbose_name='Информация о пользователе'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта',
    )
    role = models.CharField(
        default=Roles.USER,
        choices=Roles.choices,
        max_length=SLUG_FIELD_MAX_LENGTH,
        verbose_name='Уровень доступа',
    )
    username = models.CharField(
        max_length=USERNAME_FIELD_MAX_LENGTH,
        unique=True,
        validators=[
            check_username_for_me_value,
            UnicodeUsernameValidator(),
        ])

    class Meta:
        default_related_name = 'users'
        ordering = ('username', 'email')
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Returns text representation of the class."""
        return self.username

    @property
    def is_moderator(self):
        """Return True if user role is moderator, false otherwise."""
        return self.role == 'moderator'

    @property
    def is_admin(self):
        """Return True if user role is admin, false otherwise."""
        return (
            self.role == 'admin'
            or self.is_superuser
        )
