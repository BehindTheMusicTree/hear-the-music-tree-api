from rest_framework.permissions import AllowAny

from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin
from api.view.viewset.model.playlist.children.ManualPlaylistViewSet import ManualPlaylistViewSet


class ReferenceManualPlaylistViewSet(ReferenceViewSetMixin, ManualPlaylistViewSet):
    permission_classes = [AllowAny]
