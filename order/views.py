from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from common.decorator import required_role
from order.models import Order
from common.views import PostCreateModelMixin, GetListModelMixin, GetRetrieveModelMixin, PutUpdateModelMixin
from order.serializers import OrderSerializer, OrderUpdateSerializer
from user_management.models import UserProfile
from user_management.utils import send_otp


class OrderView(PostCreateModelMixin, GetListModelMixin, GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        qs = super(OrderView, self).get_queryset()
        if self.request.user == UserProfile:
            qs = qs.filter(user=self.request.user)
        return qs

    @required_role(UserProfile.CUSTOMER)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
           api to create order
        """
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
            api to get list of order
        """
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderUpdateView( PutUpdateModelMixin, GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = (AllowAny,)

    @required_role(UserProfile.SALES_AGENT)
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        """
            api to update order
        """
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()
        # send status sms message
        # send_sms()
