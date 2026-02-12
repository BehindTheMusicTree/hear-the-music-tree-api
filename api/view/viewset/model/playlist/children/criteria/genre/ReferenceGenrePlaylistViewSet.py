from rest_framework.permissions import AllowAny

from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin
from .GenrePlaylistViewSet import GenrePlaylistViewSet


class ReferenceGenrePlaylistViewSet(ReferenceViewSetMixin, GenrePlaylistViewSet):
    permission_classes = [AllowAny]
