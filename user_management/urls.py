from django.urls import path
from user_management.views import LoginViewView

urlpatterns = [
    path('admin-login/', LoginViewView.as_view()),
]
