from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from user_management.models import UserProfile, PhoneOTP
from common.views import PostCreateModelMixin, GetListModelMixin, GetRetrieveModelMixin, PutUpdateModelMixin, \
    DeleteDestroyModelMixin, success_response
from user_management.serializers import LoginSerializer, UserProfileSerializer, CustomerLoginSerializer, OTPSerializer


class LoginViewView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        """
            api for admin and sales login
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserProfile.exist_username(username=request.data['username'])
        if user:
            if not user.check_password(request.data['password']):
                raise ValidationError(detail={'user': ["username or password does not match"]})
        else:
            raise ValidationError(detail={'user': ["username does not exists"]})

        data = UserProfileSerializer(user, context={'request': request}).data
        return success_response(message="login successfully", data=data, extra_data={'token': user.get_token()})


class UserProfileView(PostCreateModelMixin, GetListModelMixin, GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (AllowAny, )

    def initial(self, request, *args, **kwargs):
        super(UserProfileView, self).initial(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
           api to create user for customer and sales - agent
        """
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(password=make_password(self.request.data['password']), is_active=False)
        # password should be sent to user on mobile or email


class UserProfileDetailView(GetRetrieveModelMixin,  GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        """
            api to get detail of user
        """
        return self.retrieve(request, *args, **kwargs)


class CustomerLoginViewView(GenericAPIView):
    serializer_class = CustomerLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        """
            api for customer login
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserProfile.exist_username(username=request.data['phone_number'])
        if user:
            PhoneOTP.check_otp(self.request.data['otp'], self.request.data['phone_number'])
        else:
            raise ValidationError(detail={'phone_number': ["phone_number does not exists"]})

        data = UserProfileSerializer(user, context={'request': request}).data
        return success_response(message="login successfully", data=data, extra_data={'token': user.get_token()})


class SendOTPView(GenericAPIView):
    serializer_class = OTPSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        """
            api for customer login
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserProfile.exist_username(username=request.data['phone_number'])
        if user:
            PhoneOTP.create_otp(self.request.data['phone_number'])
        else:
            raise ValidationError(detail={'phone_number': ["phone_number does not exists"]})
        return success_response(message="otp has been sent to register mobile number")