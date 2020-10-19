from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from common.decorator import required_role
from product.models import Product, ProductVariant
from product.serializers import ProductSerializer, ProductVariantSerializer
from common.views import PostCreateModelMixin, GetListModelMixin, GetRetrieveModelMixin, PutUpdateModelMixin
from user_management.models import UserProfile


class ProductView(PostCreateModelMixin, GetListModelMixin, GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @required_role(UserProfile.ADMIN)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
           api to create product
        """
        return self.create(request, *args, **kwargs)

    @required_role(UserProfile.ADMIN, UserProfile.CUSTOMER)
    def get(self, request, *args, **kwargs):
        """
            api to get list of product
        """
        return self.list(request, *args, **kwargs)


class ProductDetailUpdateView(GetRetrieveModelMixin, PutUpdateModelMixin, GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    @required_role(UserProfile.ADMIN, UserProfile.CUSTOMER)
    def get(self, request, *args, **kwargs):
        """
           api to update product
        """
        return self.retrieve(request, *args, **kwargs)

    @required_role(UserProfile.ADMIN)
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        """
            api to update product
        """
        return self.update(request, *args, **kwargs)


class ProductVariantView(PostCreateModelMixin, GetListModelMixin, GenericAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

    @required_role(UserProfile.ADMIN)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
           api to create product
        """
        return self.create(request, *args, **kwargs)

    @required_role(UserProfile.ADMIN, UserProfile.CUSTOMER)
    def get(self, request, *args, **kwargs):
        """
            api to get list of product
        """
        return self.list(request, *args, **kwargs)


class ProductVariantDetailUpdateView(GetRetrieveModelMixin, PutUpdateModelMixin, GenericAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

    @required_role(UserProfile.ADMIN, UserProfile.CUSTOMER)
    def get(self, request, *args, **kwargs):
        """
           api to get detail product variant
        """
        return self.retrieve(request, *args, **kwargs)

    @required_role(UserProfile.ADMIN)
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        """
            api to update product variant
        """
        return self.update(request, *args, **kwargs)





