import secrets

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """
        Переопределяем функциональность класса
    """

    use_in_migrations = True

    def create_user(self, phone_number, **extra_fields):
        """
            Создаем и сохраняем пользователя с указанным номером телефона
        """
        if not phone_number:
            raise ValueError(('Требуется ввод номера телефона'))

        user = User.objects.create(phone_number=phone_number)
        if user.referral_code is None:
            user.referral_code = secrets.token_hex(10)
            user.save()
        verification_code = User.objects.create(user=user)
        verification_code.save()

    def create_superuser(self,  phone_number, **extra_fields):
        """
            Метод создания суперпользователя
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(phone_number, **extra_fields)
        user.is_staff = extra_fields['is_staff']
        user.is_superuser = extra_fields['is_superuser']
        user.save()

        return user


class User(AbstractUser):

    username = None
    phone_number = PhoneNumberField(unique=True, verbose_name='Телефон')
    referral_code = models.CharField(max_length=10, null=True, default=None, verbose_name='Реферальный код')
    is_ref_code_generated = models.BooleanField(default=False)
    referred_to = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='has_referred', verbose_name='Приглашенный пользователь')
    is_verified = models.BooleanField(default=False, verbose_name='Верифицированный пользователь')

    verification_code = models.CharField(max_length=4, verbose_name='Код авторизации')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager() #Указываем, что все objects для класса происходят от CustomUserManager

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.phone_number




