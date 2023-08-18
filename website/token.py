from rest_framework import generics, status
from rest_framework.response import Response
from djoser import utils
from djoser.conf import settings
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")
    user_type=serializers.ReadOnlyField(source="user.first_name")
    class Meta:
        model = Token
        fields = ("auth_token","user_type")
    
class TokenCreateView(utils.ActionViewMixin, generics.GenericAPIView):
    """Use this endpoint to obtain user authentication token."""

    serializer_class = settings.SERIALIZERS.token_create
    permission_classes = settings.PERMISSIONS.token_create

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = TokenSerializer
        return Response(
            data=token_serializer_class(token).data, status=status.HTTP_200_OK
        )