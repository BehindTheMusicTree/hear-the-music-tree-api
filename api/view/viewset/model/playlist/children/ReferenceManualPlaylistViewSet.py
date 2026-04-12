from rest_framework.permissions import AllowAny

from api.view.viewset.model.playlist.children.ManualPlaylistViewSet import ManualPlaylistViewSet
from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin


class ReferenceManualPlaylistViewSet(ReferenceViewSetMixin, ManualPlaylistViewSet):
    permission_classes = [AllowAny]
