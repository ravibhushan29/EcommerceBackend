from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from user_management.models import UserProfile, PhoneOTP
from common.views import PostCreateModelMixin, GetListModelMixin, GetRetrieveModelMixin, PutUpdateModelMixin, \
    DeleteDestroyModelMixin, success_response
from user_management.serializers import LoginSerializer, UserProfileSerializer


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

