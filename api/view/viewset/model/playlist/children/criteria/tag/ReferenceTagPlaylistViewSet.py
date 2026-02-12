from rest_framework.permissions import AllowAny

from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin
from ..TagPlaylistViewSet import TagPlaylistViewSet


class ReferenceTagPlaylistViewSet(ReferenceViewSetMixin, TagPlaylistViewSet):
    permission_classes = [AllowAny]