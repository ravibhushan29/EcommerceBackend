from rest_framework import serializers

from user_management.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'username', 'role_type', 'phone_number',)

    def to_representation(self, instance):
        data = super(UserProfileSerializer, self).to_representation(instance)
        data.pop('password')
        return data

    def get_fields(self):
        fields =super(UserProfileSerializer, self).get_fields()
        if self.context['request'].method == 'PUT':
            self.Meta.read_only_fields = ('password',)
        return fields


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)


class CustomerLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)


class OTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)