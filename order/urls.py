from django.urls import path
from order.views import OrderView, OrderUpdateView
urlpatterns = [
    path('order/', OrderView.as_view()),
    path('order/<str:pk>', OrderUpdateView.as_view()),
    ]
