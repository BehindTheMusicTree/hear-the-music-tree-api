from rest_framework.permissions import AllowAny

from api.model.user.User import User
from ..TagPlaylistViewSet import TagPlaylistViewSet


class ReferenceTagPlaylistViewSet(TagPlaylistViewSet):
    permission_classes = [AllowAny]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if not request.user.is_authenticated:
            request.user = User.objects.get_system_user()