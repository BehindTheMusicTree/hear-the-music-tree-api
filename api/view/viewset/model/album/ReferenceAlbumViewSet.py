from rest_framework.permissions import AllowAny

from api.view.viewset.model.album.AlbumViewSet import AlbumViewSet
from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin


class ReferenceAlbumViewSet(ReferenceViewSetMixin, AlbumViewSet):
    permission_classes = [AllowAny]
