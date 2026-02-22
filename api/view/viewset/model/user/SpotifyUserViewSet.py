from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import MethodNotAllowed

from api.model.user.User import User
from api.serializer.model.user.spotify.output.detailed import SpotifyUserDetailedSerializer
from api.view.permission.IsAuthenticatedReturn401 import IsAuthenticatedReturn401
from api.view.viewset.model.AppModelViewSet import AppModelViewSet
from api.utils.decorators.spotify import spotify_user_required


class SpotifyUserViewSet(AppModelViewSet[User]):
    permission_classes = [IsAuthenticatedReturn401]

    def __init__(self, **kwargs):
        super().__init__(
            model_class=User,
            detailed_serializer_class=SpotifyUserDetailedSerializer,
            simple_serializer_class=SpotifyUserDetailedSerializer,
            is_private_resource=False,
            is_pk_uuid=False,
            **kwargs
        )

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return super().get_queryset().none()
        return super().get_queryset().filter(id=self.request.user.id, spotify_id__isnull=False)

    http_method_names = ["get", "head", "options"]

    @extend_schema(
        description="Get current user's Spotify profile (single item or empty list).",
        responses={
            200: SpotifyUserDetailedSerializer,
            401: {"description": "Not authenticated (1006)"},
            403: {"description": "Spotify not linked (1005)"}
        }
    )
    @spotify_user_required
    def list(self, request, *args, **kwargs):
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        raise MethodNotAllowed("GET", detail="Use GET /me/spotify/ for the current user's profile.")
