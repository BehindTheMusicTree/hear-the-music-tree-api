from rest_framework.permissions import AllowAny

from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin
from api.view.viewset.model.playlist.PlaylistViewSet import PlaylistViewSet


class ReferencePlaylistViewSet(ReferenceViewSetMixin, PlaylistViewSet):
    permission_classes = [AllowAny]
