from rest_framework.permissions import AllowAny

from api.view.viewset.model.ReferenceViewSetMixin import ReferenceViewSetMixin
from api.view.viewset.model.artist.ArtistViewSet import ArtistViewSet


class ReferenceArtistViewSet(ReferenceViewSetMixin, ArtistViewSet):
    permission_classes = [AllowAny]
