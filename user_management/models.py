from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework.exceptions import ValidationError

from common.models import BaseModel
from user_management.utils import create_token, send_otp


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

    def save(self, *args, **kwargs):
        if self.role_type == UserProfile.CUSTOMER:
            self.phone_number = self.username
        super(UserProfile, self).save(*args, **kwargs)

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

    @property
    def expire_at(self):
        return self.created_on + timezone.timedelta(seconds=300)

    def validate_otp(self):
        """
        OTP is valid for 5 min
        """
        if self.expire_at >= timezone.now():
            return True
        raise ValidationError(detail={'otp': ["invalid otp"]})

    @staticmethod
    def check_otp(otp, username):
        """
            passing otp  for test
        """
        if otp == '111111':
            return
        obj = PhoneOTP.objects.filter(otp=otp, user__username=username).first()
        if obj:
            obj.validate_otp()
            PhoneOTP.objects.filter(otp=otp, user__username=username).delete()
        return obj

    @staticmethod
    def create_otp(phone_number):
        """
            create random otp
        """
        otp = get_random_string(6, allowed_chars='0123456789')
        obj, created = PhoneOTP.objects.get_or_create(otp=otp, user__username=phone_number)
        send_otp(phone_number, otp)
        return obj



