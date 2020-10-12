from django.urls import path
from user_management.views import LoginViewView, UserProfileView

urlpatterns = [
    path('admin-login/', LoginViewView.as_view()),
    path('create-user/', UserProfileView.as_view()),
]
