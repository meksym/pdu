from django.contrib.auth.models import (
    AbstractBaseUser,
    UserManager,
    PermissionsMixin,
    Group
)
from django.contrib.auth.hashers import make_password
from django.db import models


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', unique=True)

    first_name = models.CharField(verbose_name='Ім’я', max_length=100)
    last_name = models.CharField(verbose_name='Фамілія', max_length=100)

    gender = models.CharField(
        verbose_name='Стать',
        max_length=50,
        choices=(('man', 'Чоловік'), ('woman', 'Жінка')),
        default='man'
    )

    is_staff = models.BooleanField(verbose_name='Персонал', default=False)
    is_active = models.BooleanField(
        verbose_name='Активний користувач',
        default=True
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        ordering = ['-last_login']
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            staff_group = Group.objects.get(name='Персонал (перегляд даних)')

            if (
                not self.is_superuser and
                self.is_staff and
                staff_group not in self.groups.all()
            ):
                self.groups.add(staff_group)
        except Group.DoesNotExist:
            pass
        except Group.MultipleObjectsReturned:
            pass

    def __str__(self) -> str:
        return f'Користувач {self.first_name} {self.last_name} ({self.email})'
