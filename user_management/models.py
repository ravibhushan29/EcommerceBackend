from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from common.models import BaseModel
from user_management.utils import create_token


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, password=None, role_type=None):

        if username is None:
            raise ValueError('Users must have an username.')

        user = self.model(username=username, email=self.normalize_email(email), role_type=role_type)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, email=None):

        if password is None:
            raise ValueError('Superusers must have a password.')

        user = self.create_user(username, email,  password, role_type='ADMIN')
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class UserProfile(BaseModel, AbstractUser):
    """
    customizing exist user model to add extra fields
    """
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"
    SALES_AGENT = "SALES_AGENT"
    ROLE_TYPE_CHOICE = [
        (ADMIN, 'ADMIN'),
        (CUSTOMER, 'CUSTOMER'),
        (SALES_AGENT, 'SALES_AGENT'),
    ]
    role_type = models.CharField(max_length=20, choices=ROLE_TYPE_CHOICE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    objects = UserManager()

    @staticmethod
    def exist_username(username):
        user = UserProfile.objects.filter(username=username).first()
        return user

    def get_token(self):
        return create_token(self)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"


class PhoneOTP(BaseModel):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)