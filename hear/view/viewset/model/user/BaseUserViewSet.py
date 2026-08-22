from typing import Any

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from the_music_tree_api_kit.view.viewset.model.AppModelViewSet import AppModelViewSet

from hear.model.user.User import User
from hear.serializer.model.user.base.output.detailed import UserDetailedSerializer


class BaseUserViewSet(AppModelViewSet[User]):
    serializer_class = UserDetailedSerializer
    permission_classes = [IsAdminUser]

    def __init__(self, **kwargs):
        super().__init__(
            model_class=User,
            simple_serializer_class=UserDetailedSerializer,
            detailed_serializer_class=UserDetailedSerializer,
            is_private_resource=False,
            is_pk_uuid=False,
            **kwargs,
        )

    def list(self, *args: Any, **kwargs: Any) -> Response:
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()

    def destroy(self, *args, **kwargs):
        return self._handle_destroy()
