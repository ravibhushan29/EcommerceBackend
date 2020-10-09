from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

# all mixin are override for same response

class GetListModelMixin(ListModelMixin):
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        result = {'status': {'code': status.HTTP_200_OK,
                             'message': None}
                  }
        if 'next' in response.data:  # this tells it is paginated
            result.update(response.data)
        else:
            result['data'] = response.data
        return Response(result)


class PostCreateModelMixin(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'status': {'code': status.HTTP_201_CREATED,
                                    'message': kwargs.get('message', 'Created successfully')},
                         'data': response.data
                         }, status=status.HTTP_201_CREATED)


class GetRetrieveModelMixin(RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({'status': {'code': status.HTTP_200_OK,
                                    'message': None},
                         'data': response.data
                         })


class PutUpdateModelMixin(UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({'status': {'code': status.HTTP_200_OK,
                                    'message': 'Updated successfully'},
                         'data': response.data
                         })


class DeleteDestroyModelMixin(DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'status': {'code': status.HTTP_204_NO_CONTENT,
                                    'message': 'Deleted successfully'}
                         }, status=status.HTTP_204_NO_CONTENT)


def success_response(data=None, message=None, extra_data={}):
    result = {'status': {'code': status.HTTP_200_OK,
                         'message': message},
              'data': data
              }
    result.update(extra_data)
    return Response(result)


class CustomAPIView(APIView):

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.params = request.query_params
        self.data = request.data
