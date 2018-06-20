from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def _createuser(self, **fields):
        email = fields.pop('email')
        password = fields.get('password')
        first_name = fields.get('first_name')
        last_name = fields.get('last_name')

        if email is None:
            raise ValueError('Email must not be null')
        if not first_name and not last_name:
            raise ValueError('Firstname and lastname must not be null')

        email = self.normalize_email(email=email)
        user = self.model(email=email, **fields)
        user.set_password(raw_password=password)

        user.save(using=self._db)
        return user

    def create_user(self, **fields):
        fields.setdefault('is_superuser', False)
        fields.setdefault('is_superuser', False)
        return self._createuser(**fields)

    def create_superuser(self, **fields):
        fields.setdefault('is_superuser', True)
        fields.setdefault('is_staff', True)
        return self._createuser(**fields)


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=300, null=True)
    last_name = models.CharField(max_length=300, null=True)
    email = models.CharField(max_length=300, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return f'{self.email}'
