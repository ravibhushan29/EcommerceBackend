from django.db import transaction
from rest_framework.generics import GenericAPIView
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer, CartItemUpdateSerializer
from common.decorator import required_role
from common.views import PostCreateModelMixin,  PutUpdateModelMixin
from user_management.models import UserProfile


class AddItemToCartView(PostCreateModelMixin, GenericAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    @required_role(UserProfile.CUSTOMER)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
           api to product to cart
        """
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(self.request.user, is_checkout=False)
        serializer.save(cart=cart)


class UpdateCartItemView(PutUpdateModelMixin, GenericAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemUpdateSerializer

    @required_role(UserProfile.CUSTOMER)
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        """
           api to update cart item quantity
        """
        return self.update(request, *args, **kwargs)





