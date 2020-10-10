from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from common.models import BaseModel


class UserManager(BaseUserManager):

    def create_superuser(self, username, password):

        if password is None:
            raise ValueError('Superusers must have a password.')

        user = self.create_user(username, password, user_type='ADMIN')
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

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"


class PhoneOTP(BaseModel):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)