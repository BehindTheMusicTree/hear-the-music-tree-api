from rest_framework.permissions import AllowAny

from api.view.viewset.model.playlist.PlaylistViewSet import PlaylistViewSet
from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin


class ReferencePlaylistViewSet(ReferenceViewSetMixin, PlaylistViewSet):
    permission_classes = [AllowAny]
