# external packages
from rest_framework.response import Response
from rest_framework import views
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes
)
from rest_framework import status


from .serializers import UserSerializer, User
from .utils import generate_token, decode_token


class UserSignup(views.APIView):
    http_method_names = ('post', 'get')

    def post(self, request):
        print(self.get_authenticators(), '>>>>>>>>')
        print(request.user)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'User successfully created',
            'data': serializer.data
        })

    def get(self, request):
        serializer = UserSerializer(User.objects.all(), many=True)
        if request.user.is_authenticated:
            return Response({
                'data': serializer.data
            })
        return Response({
            'message': 'User does not have permission to view this page'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def user_auth(request):
    email = request.data.get('email', None)

    if email is not None:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {
                    'error': 'Unable to generate token with supplied credentials'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        token = generate_token(user)
        return Response({'token': token})

    return Response({
        'error': 'Please provide a valid authentication credentials'
        },
        status=status.HTTP_400_BAD_REQUEST
    )


