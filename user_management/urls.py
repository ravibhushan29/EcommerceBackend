from django.urls import path
from user_management.views import LoginViewView, UserProfileView, CustomerLoginView, SendOTPView

urlpatterns = [
    path('admin-login/', LoginViewView.as_view()),
    path('create-user/', UserProfileView.as_view()),
    path('customer-login/', CustomerLoginView.as_view()),
    path('send-otp/', SendOTPView.as_view()),
]
